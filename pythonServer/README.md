# Flask Status Code Server

Tento jednoduchý Flask server umožňuje simulovat webový server pro mod balancer Apache. Server má dva endpointy, které umožňují získat a nastavit HTTP status kód a zprávu.

## Požadavky

- Python 3.x
- Flask

## Instalace

1. Klonujte repozitář nebo si stáhněte skript `server.py`.
2. Nainstalujte Flask pomocí `pip`:

    ```sh
    pip install -r requirements.txt
    ```

## Použití

1. Spusťte server s určeným portem:

    ```sh
    python server.py --port <port_number>
    ```

    Například:

    ```sh
    python server.py --port 8080
    ```

2. Endpointy:

    ### GET /state

    Vrátí aktuální status kód a zprávu.

    **Příklad použití:**

    ```sh
    curl http://127.0.0.1:<port_number>/state
    ```

    **Odpověď:**

    ```json
    {
      "status_code": 200,
      "message": "OK"
    }
    ```

    ### POST /state

    Nastaví status kód a zprávu podle zadaných parametrů.

    **Příklad použití:**

    ```sh
    curl -X POST -H "Content-Type: application/json" -d "{\"status_code\": 500, \"message\": \"code set on 500\"}" http://127.0.0.1:<port_number>/state
    ```

    **Odpověď:**

    ```json
    {
      "message": "State updated successfully"
    }
    ```

    ### GET /

    Vrátí HTML stránku s aktuálním status kódem a zprávou ve formátu moderní karty.

    **Příklad použití:**

    ```sh
    curl http://127.0.0.1:<port_number>/
    ```

    **Odpověď:**

    Otevřete URL `http://127.0.0.1:<port_number>/` ve vašem webovém prohlížeči, abyste viděli moderní kartu s názvem serveru, status kódem a zprávou.

## Příklad použití s více servery

Pro simulaci více serverů můžete spustit více instancí skriptu na různých portech:

1. Spusťte první instanci:

    ```sh
    python server.py --port 8080
    ```

2. Spusťte druhou instanci:

    ```sh
    python server.py --port 8081
    ```

3. Můžete použít curl k interakci s jednotlivými servery:

    ```sh
    curl http://127.0.0.1:8080/state
    curl http://127.0.0.1:8081/state
    ```

## Autor

Ondřej Valů

## Licence

Tento projekt je licencován pod MIT licencí.
