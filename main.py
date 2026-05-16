from src.services import(

    listar_modelos,

    cadastrar_veiculo_por_modelo,

    registrar_uso_taggy,

    listar_recompensas_catalogo
)

from src.impact_service import (

    comparar_co2,

    obter_painel_impacto,

    ranking_usuarios_verdes,

    metricas_globais
)

from src.shopcar_services import (

    cadastrar_veiculo_via_shopcar
)


# =========================================================
# MENU PRINCIPAL
# =========================================================

def menu():

    while True:

        print("\n====================================")
        print("🌱 ECOMETRIC + CAPCOINS")
        print("====================================")

        print("1 - Listar modelos")
        print("2 - Cadastrar veículo manualmente")
        print("3 - Cadastrar veículo via Shopcar API")
        print("4 - Simular impacto ambiental")
        print("5 - Registrar uso da Taggy")
        print("6 - Ver painel ambiental")
        print("7 - Ver catálogo de recompensas")
        print("8 - Ranking ESG")
        print("9 - Métricas globais ESG")
        print("0 - Sair")

        op = input("\nEscolha uma opção: ")

        # =================================================
        # LISTAR MODELOS
        # =================================================

        if op == "1":

            print("\n🚘 MODELOS DISPONÍVEIS\n")

            modelos = listar_modelos()

            for modelo in modelos:

                print(
                    f"""
ID: {modelo[0]}
Modelo: {modelo[1]}
Marca: {modelo[2]}
Ano: {modelo[3]}
Categoria: {modelo[4]}
"""
                )

        # =================================================
        # CADASTRO MANUAL
        # =================================================

        elif op == "2":

            print("\n🚘 CADASTRO MANUAL")

            placa = input("Digite a placa: ")

            modelo_id = int(
                input("Digite o ID do modelo: ")
            )

            try:

                cadastrar_veiculo_por_modelo(

                    placa,

                    modelo_id
                )

                print(
                    "\n✅ Veículo cadastrado com sucesso!"
                )

            except Exception as e:

                print(
                    f"\n❌ Erro ao cadastrar: {e}"
                )

        # =================================================
        # CADASTRO VIA SHOPCAR API
        # =================================================

        elif op == "3":

            print("\n🌐 CADASTRO VIA SHOPCAR API")

            placa = input("Placa: ")

            marca = input("Marca: ")

            modelo = input("Modelo: ")

            ano = int(
                input("Ano: ")
            )

            try:

                resultado = cadastrar_veiculo_via_shopcar(

                    placa,

                    marca,

                    modelo,

                    ano
                )

                print("\n====================================")
                print("✅ VEÍCULO CADASTRADO")
                print("====================================")

                print(
                    f"🚘 Marca: {resultado['marca']}"
                )

                print(
                    f"🚘 Modelo: {resultado['modelo']}"
                )

                print(
                    f"📅 Ano: {resultado['ano']}"
                )

                print(
                    f"⛽ Combustível: "
                    f"{resultado['combustivel']}"
                )

                print(
                    f"📂 Categoria: "
                    f"{resultado['categoria']}"
                )

                print(
                    f"🔖 Placa: "
                    f"{resultado['placa']}"
                )

            except Exception as e:

                print(
                    f"\n❌ {e}"
                )

        # =================================================
        # SIMULAÇÃO AMBIENTAL
        # =================================================

        elif op == "4":

            print("\n🌱 SIMULAÇÃO AMBIENTAL")

            placa = input(
                "Placa do veículo: "
            )

            tipo = input(
                "Tipo (shopping/pedagio/condominio/drive_thru): "
            )

            try:

                resultado = comparar_co2(

                    placa,

                    tipo
                )

                print("\n====================================")
                print("🌱 IMPACTO AMBIENTAL")
                print("====================================")

                print(
                    f"📍 Evento: {resultado['tipo']}"
                )

                print(
                    f"⛽ Combustível: "
                    f"{resultado['combustivel']}"
                )

                print(
                    f"🔋 Híbrido: "
                    f"{'Sim' if resultado['hibrido'] else 'Não'}"
                )

                print(
                    f"⏱️ Tempo poupado: "
                    f"{resultado['tempo_poupado_min']} min"
                )

                print(
                    f"⛽ Combustível poupado: "
                    f"{resultado['combustivel_poupado_ml']} ml"
                )

                print(
                    f"🌱 CO₂ evitado: "
                    f"{resultado['co2_evitar_g']} g"
                )

            except Exception as e:

                print(
                    f"\n❌ {e}"
                )

        # =================================================
        # REGISTRAR USO TAGGY
        # =================================================

        elif op == "5":

            print("\n🎯 REGISTRAR USO TAGGY")

            placa = input("Placa: ")

            tipo = input(
                "Tipo (shopping/pedagio/condominio/drive_thru): "
            )

            try:

                resultado = registrar_uso_taggy(

                    placa,

                    tipo
                )

                print("\n====================================")
                print("🎉 CAPCOINS")
                print("====================================")

                print(
                    f"💰 Pontos base: "
                    f"+{resultado['pontos_base']}"
                )

                print(
                    f"🔥 Bônus frequência: "
                    f"+{resultado['bonus']}"
                )

                print(
                    f"🏆 Total ganho: "
                    f"+{resultado['total_ganho']}"
                )

                print(
                    f"📊 Passagens no mês: "
                    f"{resultado['total_passagens_mes']}"
                )

            except Exception as e:

                print(
                    f"\n❌ {e}"
                )

        # =================================================
        # PAINEL AMBIENTAL
        # =================================================

        elif op == "6":

            print("\n📊 PAINEL AMBIENTAL")

            placa = input("Placa: ")

            try:

                painel = obter_painel_impacto(

                    placa
                )

                print("\n====================================")
                print("📊 DASHBOARD ECOMETRIC")
                print("====================================")

                print(
                    f"💰 CapCoins: "
                    f"{painel['saldo_capcoins']}"
                )

                print(
                    f"🚘 Total passagens: "
                    f"{painel['total_passagens']}"
                )

                print(
                    f"⏱️ Tempo economizado: "
                    f"{painel['tempo_total_min']} min"
                )

                print(
                    f"⛽ Combustível poupado: "
                    f"{painel['combustivel_poupado_ml']} ml"
                )

                print(
                    f"🌱 CO₂ evitado: "
                    f"{painel['co2_total_g']} g"
                )

                print(
                    f"📄 Folhas poupadas: "
                    f"{painel['folhas_poupadas']}"
                )

                print(
                    f"🌳 Equivalente árvores: "
                    f"{painel['equivalente_arvores']}"
                )

                saldo = painel[
                    "saldo_capcoins"
                ]

                if saldo >= 100:

                    print(
                        "\n🎁 Você já pode resgatar recompensas!"
                    )

                else:

                    faltam = 100 - saldo

                    print(
                        f"\n🎯 Faltam {faltam} "
                        f"CapCoins para o primeiro resgate!"
                    )

            except Exception as e:

                print(
                    f"\n❌ {e}"
                )

        # =================================================
        # CATÁLOGO DE RECOMPENSAS
        # =================================================

        elif op == "7":

            print("\n🎁 CATÁLOGO DE RECOMPENSAS\n")

            recompensas = (
                listar_recompensas_catalogo()
            )

            for recompensa in recompensas:

                print(
                    f"""
🎁 {recompensa[0]}
💰 {recompensa[1]} CapCoins
"""
                )

        # =================================================
        # RANKING ESG
        # =================================================

        elif op == "8":

            print("\n🏆 RANKING ESG\n")

            try:

                ranking = (
                    ranking_usuarios_verdes()
                )

                if not ranking:

                    print(
                        "Nenhum dado encontrado."
                    )

                else:

                    posicao = 1

                    for usuario in ranking:

                        print(
                            f"""
#{posicao}

🚘 Placa: {usuario[0]}
🌱 CO₂ evitado: {round(usuario[1], 2)} g
"""
                        )

                        posicao += 1

            except Exception as e:

                print(
                    f"\n❌ {e}"
                )

        # =================================================
        # MÉTRICAS GLOBAIS ESG
        # =================================================

        elif op == "9":

            print("\n📈 MÉTRICAS GLOBAIS ESG\n")

            try:

                metricas = metricas_globais()

                print(
                    f"""
🌱 CO₂ total evitado:
{metricas['co2_total_g']} g

⏱️ Tempo total economizado:
{metricas['tempo_total_min']} min

⛽ Combustível poupado:
{metricas['combustivel_total_ml']} ml

🌳 Equivalente em árvores:
{metricas['equivalente_arvores']}
"""
                )

            except Exception as e:

                print(
                    f"\n❌ {e}"
                )

        # =================================================
        # SAIR
        # =================================================

        elif op == "0":

            print(
                "\n👋 Encerrando sistema..."
            )

            break

        # =================================================
        # OPÇÃO INVÁLIDA
        # =================================================

        else:

            print(
                "\n❌ Opção inválida!"
            )


# =========================================================
# START SISTEMA
# =========================================================

if __name__ == "__main__":

    menu()