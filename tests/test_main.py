from fastapi.testclient import TestClient

import modelos
from base_de_datos import SessionLocal
from main import app


client = TestClient(app)


def limpiar_usuarios():
    db = SessionLocal()
    try:
        db.query(modelos.Usuario).delete()
        db.commit()
    finally:
        db.close()


def test_crud_de_usuario():
    limpiar_usuarios()

    try:
        respuesta = client.post(
            "/usuarios/",
            json={
                "nombre": "Ana",
                "apellido": "García",
                "email": "ana@example.com",
            },
        )
        assert respuesta.status_code == 200
        usuario = respuesta.json()
        assert usuario["email"] == "ana@example.com"

        usuario_id = usuario["id"]
        respuesta = client.get(f"/usuarios/{usuario_id}")
        assert respuesta.status_code == 200

        respuesta = client.put(
            f"/usuarios/{usuario_id}",
            json={
                "nombre": "Ana María",
                "apellido": "García",
                "email": "ana.maria@example.com",
            },
        )
        assert respuesta.status_code == 200
        assert respuesta.json()["nombre"] == "Ana María"

        respuesta = client.delete(f"/usuarios/{usuario_id}")
        assert respuesta.status_code == 200

        respuesta = client.get(f"/usuarios/{usuario_id}")
        assert respuesta.status_code == 404
    finally:
        limpiar_usuarios()


def test_no_permite_email_repetido():
    limpiar_usuarios()

    try:
        usuario = {
            "nombre": "Luis",
            "apellido": "Pérez",
            "email": "luis@example.com",
        }
        assert client.post("/usuarios/", json=usuario).status_code == 200
        respuesta = client.post("/usuarios/", json=usuario)
        assert respuesta.status_code == 400
    finally:
        limpiar_usuarios()
