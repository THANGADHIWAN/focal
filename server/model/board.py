from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field
from datetime import datetime

# Constants for BoardType
class BoardType(str):
    OPEN = "O"
    PRIVATE = "P"

# Constants for BoardRole
class BoardRole(str):
    NONE = ""
    VIEWER = "viewer"
    COMMENTER = "commenter"
    EDITOR = "editor"
    ADMIN = "admin"

# Constants for BoardSearchField
class BoardSearchField(str):
    NONE = ""
    TITLE = "title"
    PROPERTY_NAME = "property_name"

# Board Model
class Board(BaseModel):
    id: str
    team_id: str = Field(..., alias="teamId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    created_by: str = Field(..., alias="createdBy")
    modified_by: str = Field(..., alias="modifiedBy")
    type: BoardType
    minimum_role: BoardRole = Field(..., alias="minimumRole")
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    show_description: bool = Field(False, alias="showDescription")
    is_template: bool = Field(False, alias="isTemplate")
    template_version: int = Field(1, alias="templateVersion")  # Default version
    properties: Dict[str, Union[str, int, float, bool, List]] = Field(default_factory=dict)
    card_properties: List[Dict[str, Union[str, int, float, bool]]] = Field(default_factory=list)
    create_at: int = Field(..., alias="createAt")
    update_at: int = Field(..., alias="updateAt")
    delete_at: Optional[int] = Field(None, alias="deleteAt")

    class Config:
        allow_population_by_field_name = True

# BoardPatch Model
class BoardPatch(BaseModel):
    type: Optional[BoardType]
    minimum_role: Optional[BoardRole] = Field(None, alias="minimumRole")
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    show_description: Optional[bool] = Field(None, alias="showDescription")
    channel_id: Optional[str] = Field(None, alias="channelId")
    updated_properties: Dict[str, Union[str, int, float, bool, List]] = Field(default_factory=dict, alias="updatedProperties")
    deleted_properties: List[str] = Field(default_factory=list, alias="deletedProperties")
    updated_card_properties: List[Dict[str, Union[str, int, float, bool]]] = Field(default_factory=list, alias="updatedCardProperties")
    deleted_card_properties: List[str] = Field(default_factory=list, alias="deletedCardProperties")

    class Config:
        allow_population_by_field_name = True

# BoardMember Model
class BoardMember(BaseModel):
    board_id: str = Field(..., alias="boardId")
    user_id: str = Field(..., alias="userId")
    roles: Optional[str] = None
    minimum_role: Optional[str] = Field(None, alias="minimumRole")
    scheme_admin: bool = Field(..., alias="schemeAdmin")
    scheme_editor: bool = Field(..., alias="schemeEditor")
    scheme_commenter: bool = Field(..., alias="schemeCommenter")
    scheme_viewer: bool = Field(..., alias="schemeViewer")
    synthetic: bool

# BoardMetadata Model
class BoardMetadata(BaseModel):
    board_id: str = Field(..., alias="boardId")
    descendant_last_update_at: int = Field(..., alias="descendantLastUpdateAt")
    descendant_first_update_at: int = Field(..., alias="descendantFirstUpdateAt")
    created_by: str = Field(..., alias="createdBy")
    last_modified_by: str = Field(..., alias="lastModifiedBy")

# BoardMemberHistoryEntry Model
class BoardMemberHistoryEntry(BaseModel):
    board_id: str = Field(..., alias="boardId")
    user_id: str = Field(..., alias="userId")
    action: Optional[str] = None
    insert_at: datetime = Field(..., alias="insertAt")
