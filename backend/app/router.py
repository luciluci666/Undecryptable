from fastapi import APIRouter
from app.endpoints import EncryptedData, General, User

router = APIRouter()

router.add_api_route("/", General.root)

router.add_api_route("/register", User.register, methods=["POST"])
router.add_api_route("/login", User.login, methods=["POST"])
router.add_api_route("/refresh", User.refresh)

router.add_api_route("/data", EncryptedData.encrypt_data, methods=["POST"])
