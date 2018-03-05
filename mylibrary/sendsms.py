from .settings import APPID, APPKEY, TEMPLATE_ID
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

def send_single_sms(mobilenumber, random):
	params=[]
	params.append(random)

	ssender = SmsSingleSender(APPID, APPKEY)

	try:
	    result = ssender.send_with_param(86, mobilenumber,
	        TEMPLATE_ID, params)
	except HTTPError as e:
	    print(e)
	except Exception as e:
	    print(e)

	return result