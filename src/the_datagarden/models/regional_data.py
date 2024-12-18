import pandas as pd
import polars as pl
from datagarden_models import DataGardenModel, DatagardenModels, DataGardenSubModel, RegionalDataStats
from datagarden_models.models.base.legend import Legend
from pydantic import BaseModel

from the_datagarden.api.base import BaseApi

UNIQUE_FIELDS = [
    "region_type",
    "un_region_code",
    "iso_cc_2",
    "local_region_code",
    "local_region_code_type",
    "region_level",
    "period",
    "period_type",
    "source_name",
]
DEFAULT_COLUMNS_TO_EXCLUDE = [
    "datagarden_model_version",
    "name",
    "region_type",
    "un_region_code",
    "iso_cc_2",
    "local_region_code",
    "local_region_code_type",
    "parent_region_code",
    "parent_region_code_type",
    "parent_region_type",
    "region_level",
    "source_name",
    "data_model_name",
    "period",
    "period_type",
]


class RegionalDataRecord(BaseModel):
    name: str | None = None
    region_type: str | None = None
    un_region_code: str | None = None
    iso_cc_2: str | None = None
    local_region_code: str | None = None
    local_region_code_type: str | None = None
    parent_region_code: str | None = None
    parent_region_code_type: str | None = None
    parent_region_type: str | None = None
    region_level: int = 0
    source_name: str | None = None
    period: str | None = None
    period_type: str | None = None
    data_model_name: str | None = None
    model: DataGardenSubModel

    def record_hash(self) -> str:
        hash_str = ".".join([str(getattr(self, key)) for key in sorted(UNIQUE_FIELDS)])
        return str(hash(hash_str))

    def __str__(self):
        return (
            f"RegionalDataRecord: {self.name} ({self.data_model_name} for {self.period}, {self.period_type})"
        )

    @property
    def datgarden_model_class(self) -> type[DataGardenModel]:
        return self.model.__class__

    def record_for_sub_model(self, sub_model_name: str) -> "RegionalDataRecord":
        if sub_model_name not in self.datgarden_model_class.legends().sub_model_names:
            raise ValueError(f"Sub model `{sub_model_name}` not found in {self.datgarden_model_class}")
        child_record = self.model_dump()
        child_record["data_model_name"] = sub_model_name
        child_record["model"] = getattr(self.model, sub_model_name)
        return RegionalDataRecord(**child_record)


class TheDataGardenRegionalDataModel:
    """
    Model to hold response data from the The Data Garden API Regional Data endpoint.

    The model hold a list of regional_data records containg a regional data model
    for the region for a specific set op sources, periods and period types.

    The data can be converted to Polars and Pandas dataframes by the following
    methods:
    - to_polars(model_convertors: dict | None = None) -> pl.DataFrame
        model_convertors dict will be used to covert specifc model fields to dataframe
        columns.
    - full_model_to_polars() -> pl.DataFrame

    For pandas dataframes you can use the same methods:
    - to_pandas(model_convertors: dict | None = None) -> pd.DataFrame
    - full_model_to_pandas() -> pd.DataFrame
    """

    def __init__(
        self,
        api: "BaseApi",
        model_name: str,
        region_url: str,
        meta_data: BaseModel,
        is_sub_model: bool = False,
        model: type[DataGardenSubModel] | None = None,
    ):
        self._api: BaseApi = api
        self._model_name: str = model_name
        self._region_url: str = region_url
        self._request_params_hashes: list[str] = []
        self._data_records: dict[str, RegionalDataRecord] = {}
        self.meta_data: BaseModel = meta_data
        self._model: DataGardenModel = model or getattr(DatagardenModels, model_name.upper())
        self._is_sub_model: bool = is_sub_model

    def __str__(self):
        return f"TheDataGardenRegionalDataModel : {self._model_name} : (count={len(self._data_records)})"

    def __repr__(self):
        return self.__str__()

    def __call__(self, **kwargs) -> "TheDataGardenRegionalDataModel":
        if self._is_sub_model:
            raise TypeError(
                "Sub model data cannot be used to retrieve data. "
                "Use the main model data object to make calls to The-Datagarden API"
            )
        request_hash = self.request_hash(**kwargs)
        if request_hash not in self._request_params_hashes:
            regional_data = self.regional_paginated_data_from_api(**kwargs)
            if regional_data:
                self.set_items(regional_data)
                self._request_params_hashes.append(request_hash)
        return self

    def __getattr__(self, attribute: str) -> "TheDataGardenRegionalDataModel":
        if attribute not in self._model.legends().sub_model_names:
            raise ValueError(f"Attribute {attribute} is not a sub-model of {self._model_name}")
        sub_model = getattr(self._model.legends(), attribute).model
        regional_data_for_attribute = TheDataGardenRegionalDataModel(
            api=self._api,
            model_name=attribute,
            region_url=self._region_url,
            meta_data=self.meta_data,
            is_sub_model=True,
            model=sub_model,
        )
        regional_data_for_attribute._data_records = {
            key: value.record_for_sub_model(attribute) for key, value in self._data_records.items()
        }
        return regional_data_for_attribute

    @property
    def model_attributes(self) -> list[str]:
        return self._model.legends().attributes

    def model_attribute_legend(self, attribute: str) -> Legend:
        return getattr(self._model.legends(), attribute)

    def request_hash(self, **kwargs) -> str:
        sorted_items = sorted(kwargs.items())
        hash_str = ",".join(f"{k}:{v}" for k, v in sorted_items)
        return str(hash(hash_str))

    def _response_has_next_page(self, model_data_resp: dict) -> bool:
        pagination = model_data_resp.get("pagination", None)
        if not pagination:
            return False
        return pagination.get("next_page", None) is not None

    def _next_page_pagination(self, model_data_resp: dict) -> dict | None:
        pagination = model_data_resp.pop("pagination", None)
        if not pagination:
            return None
        next_page = pagination.get("next_page", None)
        if not next_page:
            return None
        return {"page": next_page}

    def regional_paginated_data_from_api(self, **kwargs) -> dict:
        model_data_resp = self.regional_data_from_api(**kwargs)
        if not model_data_resp:
            return {}
        while self._response_has_next_page(model_data_resp):
            next_page_pagination = self._next_page_pagination(model_data_resp)
            if next_page_pagination:
                next_page_resp = self.regional_data_from_api(pagination=next_page_pagination, **kwargs)
                if next_page_resp:
                    model_data_resp["data_by_region"].extend(next_page_resp["data_by_region"])
                    model_data_resp["pagination"] = next_page_resp["pagination"]

        return model_data_resp

    def regional_data_from_api(self, **kwargs) -> dict:
        model_data_resp = self._api.retrieve_from_api(
            url_extension=self._region_url + "regional_data/",
            method="POST",
            payload={"model": self._model_name, **kwargs},
        )
        if model_data_resp:
            return model_data_resp.json()
        return {}

    def set_items(self, data: dict):
        for regional_data in data["data_by_region"]:
            base_items = {
                "name": regional_data.get("region_name", None),
                "region_type": regional_data.get("region_type", None),
                "un_region_code": regional_data.get("un_region_code", None),
                "iso_cc_2": regional_data.get("iso_cc_2", None),
                "local_region_code": regional_data.get("local_region_code", None),
                "local_region_code_type": regional_data.get("local_region_code_type", None),
                "parent_region_code": regional_data.get("parent_region_code", None),
                "parent_region_code_type": regional_data.get("parent_region_code_type", None),
                "parent_region_type": regional_data.get("parent_region_type", None),
                "region_level": regional_data.get("region_level", 0),
            }
            data_for_region = regional_data["data_objects_for_region"]
            data_records = [
                RegionalDataRecord(**base_items, **self._record_items(data_obj))
                for data_obj in data_for_region
            ]
            for data_record in data_records:
                self._data_records.update({data_record.record_hash(): data_record})

        if self._data_records:
            _, first_record = list(self._data_records.items())[0]
            model_name = first_record.data_model_name
            if not model_name:
                raise ValueError("data_model_name is required")
            self._model_name = model_name

    def _record_items(self, data: dict):
        model_name = data.get("data_type", None)
        if not model_name:
            raise ValueError("data_model_name is required")

        model = getattr(DatagardenModels, model_name.upper())
        if not model:
            raise ValueError(f"model {model_name} not found in DatagardenModels")
        return {
            "source_name": data.get("source_name", None),
            "period": data.get("period", None),
            "period_type": data.get("period_type", None),
            "data_model_name": data.get("data_type", None),
            "model": model(**data.get("data", {})),
        }

    def to_polars(self, model_convertors: dict | None = None) -> pl.DataFrame:
        """
        Convert the data to a polars dataframe using a dictionary of model attributes to convert to columns
        """
        model_convertors = model_convertors or {}
        converted_records = []
        for record in self._data_records.values():
            model = record.model
            record_dict = record.model_dump()
            record_dict.pop("model")

            for new_col, model_attr in model_convertors.items():
                # Handle nested attributes using split by dots
                model_attr_flatten = "__flatten" in model_attr
                model_attr = model_attr.replace("__flatten", "")
                attrs = model_attr.split(".")
                value = getattr(model, attrs[0])
                for attr in attrs[1:]:
                    value = getattr(value, attr, None)
                if not value:
                    continue
                if model_attr_flatten:
                    model_data = value.model_dump() if isinstance(value, BaseModel) else value
                    record_dict.update(self.flatten_dict(model_data, {}))
                else:
                    record_dict[new_col] = value
            converted_records.append(record_dict)
        return pl.from_records(converted_records)

    def flatten_dict(self, dict_to_flatten: dict, flattened_dict: dict, prefix: str = "") -> dict:
        for key, value in dict_to_flatten.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flattened_dict.update(self.flatten_dict(value, flattened_dict, new_key))
            else:
                flattened_dict[new_key] = value

        return flattened_dict

    def full_model_to_polars(self):
        """
        Convert the data to a polars dataframe, flattening all nested dictionaries
        """
        converted_records = []
        for record in self._data_records.values():
            # Get all fields from the record excluding the modeL
            record_dict = record.model_dump(exclude={"model"})
            # Model data is added as flattened dictionary
            model_data = record.model.model_dump()
            flattened_dict = self.flatten_dict(model_data, {})
            record_dict.update(flattened_dict)
            converted_records.append(record_dict)
        return pl.from_records(converted_records)

    def to_pandas(self, model_convertors: dict | None = None) -> pd.DataFrame:
        """
        Convert the data to a pandas dataframe using a dictionary of model attributes to convert to columns
        """
        return self.to_polars(model_convertors).to_pandas()

    def full_model_to_pandas(self) -> pd.DataFrame:
        """
        Convert the data to a pandas dataframe, flattening all nested dictionaries
        """
        return self.full_model_to_polars().to_pandas()

    def __iter__(self):
        """Makes the class iterable over the values in _data_records"""
        return iter(self._data_records.values())

    def __len__(self):
        """Returns the number of records"""
        return len(self._data_records)

    @property
    def data_records(self) -> list[RegionalDataRecord]:
        return list(self._data_records.values())

    def regional_availability(self) -> dict[str, RegionalDataStats | None]:
        availability_per_region = self.meta_data.statistics_for_data_model(model_name=self._model_name)
        regional_availability = {}
        for region_type in self.meta_data.region_types:
            if region_type in availability_per_region.keys():
                regional_availability[region_type] = availability_per_region[region_type]
            else:
                regional_availability[region_type] = None
        return regional_availability

    @property
    def regions_with_model_data(self) -> list[str]:
        return [region for region in self.regional_availability() if self.regional_availability()[region]]

    def show_summary(self):
        """
        Outputs a summary of the model's structure (submodels and attributes)
        """
        self._model.legends().show_summary()

    def summary(self) -> dict:
        """
        return model's structure (submodels and attributes)
        """
        return self._model.legends().summary()

    def describe(
        self,
        include_attributes: list[str] | None = None,
        exclude_attributes: list[str] | None = None,
        filter_expr: pl.Expr | None = None,
    ) -> pl.DataFrame:
        df = self.full_model_to_polars()
        if df.is_empty():
            raise ValueError("No data loaded for this model. Data is needed to describe the model.")

        if filter_expr is not None:
            df = df.filter(filter_expr)

        if include_attributes:
            return df.select(include_attributes).describe()

        attributes_to_exclude = DEFAULT_COLUMNS_TO_EXCLUDE.copy()
        if exclude_attributes:
            attributes_to_exclude.extend(exclude_attributes)
        return df.select([col for col in df.columns if col not in attributes_to_exclude]).describe()

    def data_availability_per_attribute(
        self, include_attributes: list[str] | None = None, filter_expr: pl.Expr | None = None
    ):
        if include_attributes:
            describe_df = self.describe(include_attributes=include_attributes, filter_expr=filter_expr)
        else:
            describe_df = self.describe(
                exclude_attributes=DEFAULT_COLUMNS_TO_EXCLUDE, filter_expr=filter_expr
            )

        describe_df = describe_df.with_columns(
            pl.when(pl.col("statistic").is_in(["count", "null_count"]))
            .then(pl.all().exclude("statistic").cast(pl.Int64))
            .otherwise(pl.all().exclude("statistic"))
        )

        return describe_df

    def show_data_availability_per_attribute(
        self, include_attributes: list[str] | None = None, filter_expr: pl.Expr | None = None
    ):
        describe_df = self.data_availability_per_attribute(include_attributes, filter_expr)
        stats_by_column = {
            column: dict(
                zip(describe_df.get_column("statistic"), describe_df.get_column(column), strict=True)
            )
            for column in describe_df.columns
            if column != "statistic"
        }

        max_column_length = max(len(column) for column in stats_by_column.keys())

        for column, stats in stats_by_column.items():
            print(
                f"{column} : {" " * (max_column_length + 3 - len(column))}"
                f"{int(stats['count'] + stats['null_count'])}"
                f" of which with data: {int(stats['count'])} "
                f"({int(stats['count']) / (int(stats['count'] + stats['null_count'])) * 100:.0f}%)"
            )
