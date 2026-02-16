from pydantic import BaseModel, Field, model_validator


class Configuration(BaseModel):
    header_types: list[type] = Field(default=[])

    trate_nullerror: bool = Field(default=False)
    trate_typeerror: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_types(self):
        if self.trate_typeerror and not self.header_types:
            raise ValueError("Can not apply type validator if header_type is empty.")

        if self.header_types and not self.trate_typeerror:
            raise ValueError("If header_type is empty can not apply type validator.")

        return self
