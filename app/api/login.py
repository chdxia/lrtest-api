from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from ..database.mysql import get_mysql_db
from ..crud import user_crud
from ..schemas import user_schemas
from ..dependencies import role_depends
from ..lib import str_to_selt_sha256


router = APIRouter(
    tags=['登录']
)

@router.post('/login', summary='登录')
async def login(body: user_schemas.UserLogin, db_session: Session=Depends(get_mysql_db)): # 支持账号or邮箱登录
    db_user = user_crud.get_user_by_account(db_session, account=body.account)
    if db_user is None: # 账号登录失败，尝试使用邮箱登录
        db_user_email = user_crud.get_user_by_email(db_session, email=body.account)
        if db_user_email is None: # 邮箱登录失败
            raise HTTPException(status_code=400, detail='Account or password is incorrect')
        elif not db_user_email.status: # 账户已停用
            raise HTTPException(status_code=400, detail='Account is disabled')
        elif db_user_email.password == str_to_selt_sha256(body.password, db_user_email.password.split('$')[2]): # 密码正确，更新token
            return {"code": 20000, "message": "success", "data":{"token": user_crud.update_token(db_session, db_user_email.id)}}
        else:
            raise HTTPException(status_code=400, detail='Account or password is incorrect')
    elif not db_user.status: # 账户已停用
        raise HTTPException(status_code=400, detail='Account is disabled')
    elif db_user.password == str_to_selt_sha256(body.password, db_user.password.split('$')[2]): # 密码正确，更新token
        return {"code": 20000, "message": "success", "data":{"token": user_crud.update_token(db_session, db_user.id)}}
    else:
        raise HTTPException(status_code=400, detail='Account or password is incorrect')


@router.delete('/logout', summary='退出登录', dependencies=[Depends(role_depends())])
async def logout(X_Token: str=Header(None) , db_session: Session=Depends(get_mysql_db)):
    if X_Token: # 清空token
        user_crud.update_token(db_session, access_token=X_Token)
    return {"code": 20000, "message": "success"}