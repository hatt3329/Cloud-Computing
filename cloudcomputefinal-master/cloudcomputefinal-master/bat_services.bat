@echo off

REM Start each FastAPI service using python -m uvicorn
start cmd /k "python -m uvicorn service1_user_auth:app --port 8001 --reload"
start cmd /k "python -m uvicorn service2_vendor_auth:app --port 8002 --reload"
start cmd /k "python -m uvicorn service3_product_search:app --port 8003 --reload"
start cmd /k "python -m uvicorn service4_profile_logout:app --port 8004 --reload"
start cmd /k "python -m uvicorn service5_reviews:app --port 8005 --reload"
start cmd /k "python -m uvicorn service6_product_mgmt:app --port 8006 --reload"
start cmd /k "python -m uvicorn service7_cart:app --port 8007 --reload"
start cmd /k "python -m uvicorn service8_order:app --port 8008 --reload"
start cmd /k "python -m uvicorn service9_vendor_profile:app --port 8009 --reload"
start cmd /k "python -m uvicorn service10_return:app --port 8010 --reload"

echo All services launched.
pause

