
from django.http import Http404

from restapp.serializers import UserSerializer, AndroidGroupMsgSerializer, AndroidErrMsgSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
import json
from libs.official_account import OfficialAccount


import logging
logger = logging.getLogger(__name__)



class feedback(APIView):

    def post(self, request):
        return Response({})


class getNewsContent(APIView):

    def get(self, request):
        id = request.GET.get('id', 0)
        oaObj = OfficialAccount()
        data = oaObj.getAppNewsContent(id=id)

        if not data:
            return Response({})
        else:
            result = {'err_msg': 'success', 'data': data, 'info': "\u8bfb\u53d6\u4fe1\u606f\u5217\u8868\u6210\u529f\uff01"}
            return Response(result)

class getOAList(APIView):

    def get(self, request):
        table = request.GET.get('table', "")
        query = request.GET.get('query', "")
        pageSize =  int(request.GET.get('pageSize', 20))
        pageIndex =  int(request.GET.get('pageIndex', 1)) - 1
        classid =  int(request.GET.get('classid', 0))

        if table and query == "":

            location = 0
            limit = pageSize
            sort = 0
            robot_username = []
            day = 300

            oaObj = OfficialAccount()
            if location == 1:
                robot_username = oaObj.getDisplayRobotUsernames('US')
            elif location == 2:
                robot_username = oaObj.getDisplayRobotUsernames('CA')

            order = ''
            if sort == 1:
                order = ' order by sum(b.read_number) desc  '
            elif sort == 2:
                order = ' order by average_read_number desc  '

            accounts = oaObj.getOARank(day, robot_username, order, page_start=pageIndex, limit=limit)

            data = []
            for account in accounts:
                data.append({'classid':str(classid), 'id':str(account['id']), 'name':str(account['nick_name']), 'head_image':str(account['head_image']),
                             'total_read':str(account['total_read']), 'average_read_number':str(account['average_read_number']),
                             'daily_pub_num':str(account['daily_pub_num'])})

            result = {'err_msg': 'success', 'data':data, 'total': '10546', 'pageTotal':528, "pageIndex":pageIndex, "pageSize":pageSize, 'classid':'0'}

            return Response(result)
        else:
            return Response({})

class getNewsList(APIView):

    def get(self, request):
        table = request.GET.get('table', "")
        query = request.GET.get('query', "")
        pageSize =  int(request.GET.get('pageSize', 20))
        pageIndex =  int(request.GET.get('pageIndex', 1)) - 1
        classid =  int(request.GET.get('classid', 0))

        if table and query == "":

            robot_username = []

            oaObj = OfficialAccount()

            if classid == 1 or classid == 5:
                robot_username = oaObj.getDisplayRobotUsernames('US')
            elif classid == 2 or classid == 6:
                robot_username = oaObj.getDisplayRobotUsernames('CA')

            extra = ' order by pub_time desc'
            if classid == 0 or classid == 1 or classid == 2:
                extra = " and pub_time > (UNIX_TIMESTAMP() - 24*3600) order by read_number DESC "
            elif classid == 4 or classid == 5 or classid == 6:
                extra = " and pub_time > (UNIX_TIMESTAMP() - 48*3600) order by related_number desc, read_number desc "
            elif classid == 7:
                extra = ' order by pub_time desc'

            data = oaObj.getAppNewsList(page_start=pageIndex * pageSize, limit=pageSize, robot_usernames=robot_username, extra=extra)


            result = {}
            #result['error_msg'] = str('success')
            #result['data'] = data

            #result['total'] = '10546',


            #result["pageTotal"] = "528",
            #result["pageIndex"] = 1,
            #result["pageSize"] = 2,
            #result["classid"] = '0',
            #result["adverNewsList"] = "<a href='http:\/\/www.baidu.com' title='\u6d4b\u8bd5\u5e7f\u544a' class='external brower'>\u6d4b\u8bd5\u5e7f\u544a<\/a>",
            #result["info"] = "\u8bfb\u53d6\u4fe1\u606f\u5217\u8868\u6210\u529f\uff01"


            result = {'err_msg': 'success', 'data':data, 'total': '10546', 'pageTotal':528, "pageIndex":1, "pageSize":2, 'classid':'0',
                      'adverNewsList':"<a href='http://www.baidu.com' title='\u6d4b\u8bd5\u5e7f\u544a' class='external brower'>\u6d4b\u8bd5\u5e7f\u544a<\/a>",
                      'info':"\u8bfb\u53d6\u4fe1\u606f\u5217\u8868\u6210\u529f\uff01"}


            return Response(result)
        else:
            return Response({})
            #return Response({}, status=status.HTTP_400_BAD_REQUEST)