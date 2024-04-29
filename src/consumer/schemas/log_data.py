from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class LogDataSchema(BaseModel):
    partition: str
    ID: str = Field(default_factory=lambda: str(uuid4()), validate_default=True)

    model_config = ConfigDict(extra='allow')

    @field_validator("ID", mode="after")
    def add_partition_id(cls, value: str, info: ValidationInfo):
        return f"{info.data.get('partition')}:{value}"
