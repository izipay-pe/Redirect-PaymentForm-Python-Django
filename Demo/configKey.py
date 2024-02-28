# Identificador de su tienda
SHOP_ID = "~~CHANGE_ME_BACKOFFICE_SHOP_ID~~"

# Clave de TEST O PRODUCCIÓN de su tienda.
TEST_KEY = "~~CHANGE_ME_BACKOFFICE_TEST_PASSWORD~~"
PROD_KEY = "~~CHANGE_ME_BACKOFFICE_PROD_PASSWORD~~"

# URL del servidor de Izipay
URL_IZIPAY = "https://secure.micuentaweb.pe/vads-payment/"

# Modo de configuración
MODE = "TEST"

# Verificar Modo
if MODE == "TEST":
    KEY = TEST_KEY
elif MODE == "PROD":
    KEY = PROD_KEY
