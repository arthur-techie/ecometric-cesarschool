import requests
import time


# =========================================================
# CONFIG
# =========================================================

BASE_URL = "https://shopcar-api.onrender.com"


# =========================================================
# TESTE
# =========================================================

def testar_api():

    print("\n=================================================")
    print("TESTE SHOPCAR API")
    print("=================================================")

    urls = [

        BASE_URL,

        f"{BASE_URL}/docs",

        f"{BASE_URL}/openapi.json"
    ]

    for url in urls:

        print("\n=================================================")
        print(f"TESTANDO: {url}")
        print("=================================================")

        try:

            inicio = time.time()

            response = requests.get(

                url,

                timeout=60
            )

            fim = time.time()

            print(f"\nSTATUS: {response.status_code}")

            print(f"\nTEMPO:")
            print(f"{round(fim - inicio, 2)} segundos")

            print("\nCONTENT-TYPE:")
            print(
                response.headers.get(
                    "Content-Type"
                )
            )

            print("\nRESPOSTA:")
            print(response.text[:1500])

        except requests.exceptions.Timeout:

            print("\n⏱️ TIMEOUT")

        except Exception as e:

            print(f"\n❌ ERRO: {e}")


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    testar_api()