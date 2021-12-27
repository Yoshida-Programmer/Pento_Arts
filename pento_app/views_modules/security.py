#--ハッシュ値生成--------------------------------------
import uuid

def set_submit_token(request):
    #ハッシュ値生成
    submit_token = str(uuid.uuid4())
    #セッションにトークンを格納
    request.session['submit_token'] = submit_token
    #クライアント用に同じ値のトークンを返す
    return submit_token

def exist_submit_token(request):
    #クライアントから送信されたトークンを取得
    token_in_request = request.POST.get('submit_token')
    #一度使用したトークンだった場合セッションから破棄
    token_in_session = request.session.pop('submit_token', '')

    if not token_in_request:
        return False
    if not token_in_session:
        return False

    return token_in_request == token_in_session