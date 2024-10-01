# permissions.py

class Permission:
    def __init__(self, id: str, name: str = "", description: str = "", scope: str = ""):
        self.id = id
        self.name = name
        self.description = description
        self.scope = scope

# Define permissions as constants
PermissionViewTeam = "view_team"
PermissionManageTeam = "manage_team"
PermissionManageSystem = "manage_system"
PermissionReadChannel = "read_channel"
PermissionCreatePost = "create_post"
PermissionViewMembers = "view_members"
PermissionCreatePublicChannel = "create_public_channel"
PermissionCreatePrivateChannel = "create_private_channel"
PermissionManageBoardType = Permission(id="manage_board_type")
PermissionDeleteBoard = Permission(id="delete_board")
PermissionViewBoard = Permission(id="view_board")
PermissionManageBoardRoles = Permission(id="manage_board_roles")
PermissionShareBoard = Permission(id="share_board")
PermissionManageBoardCards = Permission(id="manage_board_cards")
PermissionManageBoardProperties = Permission(id="manage_board_properties")
PermissionCommentBoardCards = Permission(id="comment_board_cards")
PermissionDeleteOthersComments = Permission(id="delete_others_comments")



# main.py
from fastapi import FastAPI, HTTPException
from permissions import (
    PermissionViewTeam,
    PermissionManageTeam,
    PermissionManageSystem,
    PermissionReadChannel,
    PermissionCreatePost,
    PermissionViewMembers,
    PermissionCreatePublicChannel,
    PermissionCreatePrivateChannel,
    PermissionManageBoardType,
    PermissionDeleteBoard,
    PermissionViewBoard,
    PermissionManageBoardRoles,
    PermissionShareBoard,
    PermissionManageBoardCards,
    PermissionManageBoardProperties,
    PermissionCommentBoardCards,
    PermissionDeleteOthersComments,
)

app = FastAPI()

@app.get("/permissions/")
async def get_permissions():
    return {
        "permissions": {
            "view_team": PermissionViewTeam,
            "manage_team": PermissionManageTeam,
            "manage_system": PermissionManageSystem,
            "read_channel": PermissionReadChannel,
            "create_post": PermissionCreatePost,
            "view_members": PermissionViewMembers,
            "create_public_channel": PermissionCreatePublicChannel,
            "create_private_channel": PermissionCreatePrivateChannel,
            "manage_board_type": PermissionManageBoardType.id,
            "delete_board": PermissionDeleteBoard.id,
            "view_board": PermissionViewBoard.id,
            "manage_board_roles": PermissionManageBoardRoles.id,
            "share_board": PermissionShareBoard.id,
            "manage_board_cards": PermissionManageBoardCards.id,
            "manage_board_properties": PermissionManageBoardProperties.id,
            "comment_board_cards": PermissionCommentBoardCards.id,
            "delete_others_comments": PermissionDeleteOthersComments.id,
        }
    }
