# main.py
import json
import math
from fastapi import FastAPI,Request 
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import crud
import json
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from decimal import Decimal
from datetime import datetime, date

app = FastAPI()
@app.middleware("http")
async def method_not_allowed_middleware(request: Request, call_next):
    if request.url.path == "/v1/Auth/login" and request.method != "POST":
        save_logs(request.url.path, request.method, "URLHIT", "127.0.0.1")
        return JSONResponse(
            content={"error": f"{request.method} Method Not Allowed"},
            status_code=405
        )
    if request.url.path == "/v1/Auth/createAcc" and request.method != "POST":
        return JSONResponse(
            content={"error": f"{request.method} Method Not Allowed"},
            status_code=405
        )
    if request.url.path == "/v1/Transactions/generateTxn" and request.method != "POST":
        return JSONResponse(
            content={"error": f"{request.method} Method Not Allowed"},
            status_code=405
        )
    if request.url.path == "/v1/Transations/transactions" and request.method != "POST":
        return JSONResponse(
            content={"error": f"{request.method} Method Not Allowed"},
            status_code=405
        )
    response = await call_next(request)
    return response

@app.post("/v1/Auth/createAcc")
async def create_user_endpoint(request: Request):
    try:
        requestData = await request.json()
        isNull,key = checkNull(requestData)
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    if not requestData:
        return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
    try:
        response = crud.turtleInsert("CREATEUSER", requestData)
        save_logs(json.dumps(requestData), json.dumps(response), "CREATEUSER", "127.0.0.1")
        if response:
             return JSONResponse(content={"message": "Create Successfull"}, status_code=200)
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"CREATEUSER","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)


@app.post("/v1/Auth/login")
async def loginUser(request: Request):
    try:
        requestData = await request.json()
        isNull,key = checkNull(requestData)
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    if not requestData:
        return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
    try:
        response,data = crud.read_data_with_Specific("LOGINUSER","*",requestData,True)
        if response:
            storeData = jsonable_encoder(data)
            save_logs(json.dumps(requestData),json.dumps(storeData),"LOGINUSER","127.0.0.1")
            if data and data['usr_status'] == 0:
             return JSONResponse(
                content={"status": "success", "data": jsonable_encoder(data)},
                status_code=200
            )
            else:
                return JSONResponse(
                    content={"status": "error", "message": "User is inactive"},
                    status_code=403
                )
        else:
            return JSONResponse(
                content={"status": "error", "message": "User not found"},
                status_code=401
            )   
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"LOGINUSER","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)
    
@app.post("/v1/Goal/goals")
async def getAllGoals(request: Request):
    try:
        requestData = await request.json()
        isNull,key = checkNull(requestData)
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=200
        )
    if not requestData:
        return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=200
        )
    try:
        response,data = crud.read_data("GETGOALS","*",requestData,False)
        if response:
            storeData = jsonable_encoder(data)
            save_logs(json.dumps(requestData),json.dumps(storeData),"GETGOALS","127.0.0.1")
            return JSONResponse(
                content={"status": "success", "data": jsonable_encoder(data)},
                status_code=200
            )
        else:
                return JSONResponse(
                    content={"status": "error", "message": "User is inactive"},
                    status_code=403
                )
        
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"GETGOALS","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.post("/v1/Transactions/generateTxn")
async def generate_Transaction(request: Request):
    try:
        requestData = await request.json()
        isNull,key = checkNull(requestData)
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )

    try:
        response = crud.turtleInsert("GENERATETXN", requestData)
        save_logs(json.dumps(requestData), json.dumps(response), "GENERATETXN", "127.0.0.1")
        if response:
             return JSONResponse(content={"message": "Transaction Generated"}, status_code=200)
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"GENERATETXN","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.post("/v1/Transactions/transactions")
async def getAllTransactions(request: Request):
    try:
        requestData = await request.json()
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=401
        )
        isNull,key = checkNull(requestData)
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    try:
        response,data = crud.read_data_with_Specific("GETTXN","*",requestData,False)
        if response:
            storeData = jsonable_encoder(data)
            save_logs(json.dumps(requestData),json.dumps(storeData),"GETTXN","127.0.0.1")
            return JSONResponse(
                content={"status": "success", "data": jsonable_encoder(data)},
                status_code=200
            )
        else:
                return JSONResponse(
                    content={"status": "error", "message": "No Data Found"},
                    status_code=403
                )
        
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"GETTXN","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=200)


@app.post("/v1/Goal/createGoal")
async def create_goal_endpoint(request: Request):
    try:
        requestData = await request.json()
        isNull,key = checkNull(requestData)
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    if not requestData:
        return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
    try:
        response = crud.turtleInsert("CREATEGOAL", requestData)
        save_logs(json.dumps(requestData), json.dumps(response), "CREATEGOAL", "127.0.0.1")
        if response:
             return JSONResponse(content={"message": "Create Successfull"}, status_code=200)
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"CREATEGOAL","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)
    
@app.post("/v1/Goal/joinGoals")
async def create_goal_endpoint(request: Request):
    try:
        requestData = await request.json()
        isNull,key = checkNull(requestData)
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    if not requestData:
        return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=400
        )
    try:
        response = crud.turtleInsert("JOINGOAL", requestData)
        save_logs(json.dumps(requestData), json.dumps(response), "JOINGOAL", "127.0.0.1")
        if response:
             return JSONResponse(content={"message": "Create Successfull"}, status_code=200)
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"JOINGOAL","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.post("/v1/Goal/Calculate")
async def calculate_goal_endpoint(request: Request):
    try:
        requestData = await request.json()
        isNull, key = checkNull(requestData)
        if not requestData:
            return JSONResponse(
                content={"error": "Request body cannot be empty"},
                status_code=400
            )
        if isNull:
            return JSONResponse(
                content={"error": "Parameter cannot be null or empty", "Parameter": key},
                status_code=400
            )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )

    totalPeriodsRequired = 0
    completion_date = None
    dailyInvest = None
    try:
        totalUser = int(requestData.get('totaluser', 0))
        goalamount = float(requestData.get('goalMoney', 0))
        perUserInvest = float(requestData.get('perUserInvest', 0))  # how much 1 user invests (daily/weekly)
        totalContribution = perUserInvest * totalUser

        if totalContribution > 0:
            if requestData.get('investType') == 0:  # Daily
                totalPeriodsRequired = math.ceil(goalamount / totalContribution)
                delta = timedelta(days=totalPeriodsRequired)
                dailyInvest = perUserInvest
            elif requestData.get('investType') == 1:  # Weekly
                totalPeriodsRequired = math.ceil(goalamount / totalContribution)
                delta = timedelta(weeks=totalPeriodsRequired)
                dailyInvest = perUserInvest / 7  # optional: daily equivalent
            else:
                totalPeriodsRequired = None
                delta = None
                dailyInvest = None

            if totalPeriodsRequired:
                start_date_str = requestData.get('startDate', datetime.now().strftime('%Y-%m-%d'))
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                completion_date = start_date + delta

        save_logs(json.dumps(requestData), json.dumps(totalPeriodsRequired), "GOALCALCULATION", "127.0.0.1")

        if totalPeriodsRequired:
            return JSONResponse(
                content={
                    "totalPeriodsRequired": totalPeriodsRequired,
                    "completionDate": completion_date.strftime('%Y-%m-%d') if completion_date else None,
                    "investment_type": requestData.get('investType'),
                    "investAmt": goalamount,
                    "dailyinvest": dailyInvest,
                    "totalUser": totalUser
                },
                status_code=200
            )
        else:
            return JSONResponse(
                content={"error": "Invalid input or cannot calculate periods."},
                status_code=400
            )

    except Exception as e:
        save_logs(json.dumps(requestData), json.dumps({"error": str(e)}), "GOALCALCULATION", "127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.post("/v1/Contributors/AllContributors")
async def getAllTransactions(request: Request):
    try:
        requestData = await request.json()
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=401
        )
        isNull,key = checkNull(requestData)
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    try:
        response,data = crud.read_data_using_multiple_source("CONTRIBUTORS","*",requestData,False,"users","id","uid")
        if response:
            storeData = jsonable_encoder(data)
            save_logs(json.dumps(requestData),json.dumps(storeData),"CONTRIBUTORS","127.0.0.1")
            return JSONResponse(
                content={"status": "success", "data": jsonable_encoder(data)},
                status_code=200
            )
        else:
                return JSONResponse(
                    content={"status": "error", "message": "No Data Found"},
                    status_code=403
                )
        
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"CONTRIBUTORS","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)
    
    
@app.post("/v1/Goal/getGoalDetails")
async def getGoalDetails(request: Request):
    try:
        requestData = await request.json()
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=401
        )
        isNull,key = checkNull(requestData)
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    try:
        response,data = crud.read_data_using_multiple_source("GETGOAL","goal_db_id,goal_amt,total_save,goal_name",requestData,True,'goals','id','goal_db_id')
        if response:
            storeData = jsonable_encoder(data)
            save_logs(json.dumps(requestData),json.dumps(storeData),"GETGOAL","127.0.0.1")
            return JSONResponse(
                content={"status": "success", "data": jsonable_encoder(data)},
                status_code=200
            )
        else:
                return JSONResponse(
                    content={"status": "error", "message": "No Data Found"},
                    status_code=403
                )
        
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"GETGOAL","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)
    

@app.post("/v1/Goal/JoinGoal")
async def joinGoal(request: Request):
    try:
        requestData = await request.json()
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=401
        )
        isNull,key = checkNull(requestData)
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    try:
        check_filter = {
            "uid": requestData.get("uid"),
            "goal_db_id": requestData.get("goal_db_id"),
        }
        checkResponse,data = crud.read_data_with_Specific("CHECKALREADYJOIN","*",check_filter,True)
        if checkResponse:
            if str(data['uid']) == str(requestData.get("uid")):
                return JSONResponse(
                    content={"status": "error", "message": "User already joined this goal"},
                    status_code=403
                )
            else:
             return JSONResponse(
                content={"status": "success", "data": "Something went wrong"},
                status_code=200
            )
        else:
            response = crud.turtleInsert("JOINGOAL",requestData)
            storeData = jsonable_encoder(response)
            save_logs(json.dumps(requestData),json.dumps(storeData),"JOINGOAL","127.0.0.1")
            return JSONResponse(
                content={"status": "success", "data": "Join Successfull"},
                status_code=200
            )
        
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"JOINGOAL","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.post("/v1/Goal/Calculation")
async def joinGoal(request: Request):
    try:
        requestData = await request.json()
        if not requestData:
            return JSONResponse(
            content={"error": "Request body cannot be empty"},
            status_code=401
        )
        isNull,key = checkNull(requestData)
        if isNull:
            return JSONResponse(
            content={"error": "Parameter cannot be null or empty", "Parameter": key},
            status_code=400
        )
    except Exception:
        return JSONResponse(
            content={"error": "Invalid or empty request body"},
            status_code=400
        )
    try:
        check_filter = {
            "uid": requestData.get("uid"),
            "goal_db_id": requestData.get("goal_db_id"),
        }
        checkResponse,data = crud.read_data_with_Specific("CHECKALREADYJOIN","*",check_filter,True)
        if checkResponse:
            if str(data['uid']) == str(requestData.get("uid")):
                return JSONResponse(
                    content={"status": "error", "message": "User already joined this goal"},
                    status_code=403
                )
            else:
             return JSONResponse(
                content={"status": "success", "data": "Something went wrong"},
                status_code=200
            )
        else:
            response = crud.turtleInsert("JOINGOAL",requestData)
            storeData = jsonable_encoder(response)
            save_logs(json.dumps(requestData),json.dumps(storeData),"JOINGOAL","127.0.0.1")
            return JSONResponse(
                content={"status": "success", "data": "Join Successfull"},
                status_code=200
            )
        
    except Exception as e:
        save_logs(json.dumps(requestData),json.dumps({"error": str(e)}),"JOINGOAL","127.0.0.1")
        return JSONResponse(content={"message": str(e)}, status_code=500)




def calculate_share_amt(goal_id, uid):
    if goal_id is None or uid is None:
        raise ValueError("goal_id and uid must be provided")
    else:
        response,data = crud.read_data_with_Specific("GETGOAL","*",{"id":goal_id},True)
        if response:
            return data
        else:
            return 0


def save_logs(m_snd,m_reci,m_api,m_ip):
        return crud.save_log({
            "m_snd": m_snd,
            "m_reci": m_reci,
            "m_api": m_api,
            "m_ip": m_ip
        })
def phoneNumberValidation(phone):
    if len(phone) != 10 or not phone.isdigit():
        return False
    if alphaNumericValidation(phone):
        return True
    return False

def alphaNumericValidation(value):
    return value.isalnum()

def checkNull(requestData: dict):
    for key, value in requestData.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return True, key
    return False, None
def convertedResponse(code,status,response):
    return {
        "code":code,
        "status":status,
        "response":response
    }