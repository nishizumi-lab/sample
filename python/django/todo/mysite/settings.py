import os

# プロジェクト内にパスを作成
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 秘密鍵
SECRET_KEY = '5^ig7!vuiy&xti4uh9y&1-zxn8+guo0ex5(fh&a*7ghgq9z=a%'

# デバッグモードの有効化（リリース時はデバッグをオフにする）
DEBUG = True

# リリース時は公開するサイトのドメイン名（*.example.com）を入れる
ALLOWED_HOSTS = ['*']

# 利用するアプリケーションの定義
# データベースのマイグレーションファイル作成の際などに利用
INSTALLED_APPS = [
    'django.contrib.admin', 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles',  # ↑デフォルトのアプリ
    'todo.apps.TodoConfig', # ★ 今回は新たにtodoアプリを作成して追加するので、ここに追記
]

# 有効化するMiddlewareクラス（リクエスト/レスポンス処理にhookを加えるための仕組み）
# HTTP 要求を受け取ったり、HTTP 応答を返却する際に、ここで定義したミドルウェアを順次実行
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ルートディレクトリの設定（モジュールでどの設定を使うか指定）
# 下記の場合、./mysite/urls.py を指定
ROOT_URLCONF = 'mysite.urls'

# テンプレートに関する定義
# BACKEND:テンプレートエンジン
# DIRS:テンプレートを探す対象のフォルダリスト
# APP_DIRS:アプリケーションフォルダ配下を探すか否かのフラグ
# OPTIONS:各種オプション情報
# context_processors:テンプレートで参照可能な変数を生成するプロセッサ群
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI のアプリケーションを指定
# 下記の場合は ./mysite/wsgi.py のapplication を指定
WSGI_APPLICATION = 'mysite.wsgi.application'


# データベースに関する定義
# SQLite3, MySQL(MariaDB), PostgreSQL, Oracle など利用可能
# 下記の場合、sqlite3を選択し、./db.sqlite3に生成
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# パスワードのバリデーションルール(禁止ルール)を指定
# 下記の場合、ユーザ名と似たパスワード、パスワード長、よくあるパスワード、数値のみのパスワードをチェック
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# デフォルトの言語を指定
# ★日本語と英語を選択
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja-JP'

# タイムゾーン
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo' # ★タイムゾーンを東京に変更

# 多言語化機能を有効にするか否かを指定(I18N:internationalisation の略)
USE_I18N = True

# 日付フォーマットなどのローカライゼーション機能を有効にするか否かを指定(L10N:localization の略)
USE_L10N = True

# タイムゾーン変換機能を有効にするか否かを指定
USE_TZ = True


# スタティックファイル (CSS, JavaScript, Images)の URL を指定
STATIC_URL = '/static/'
