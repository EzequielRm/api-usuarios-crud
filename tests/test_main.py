import os

os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-key-that-is-long-enough")

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


def registrar_usuario(nombre, apellido, email, password="clave-segura-123"):
    return client.post(
        "/usuarios/",
        json={
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "password": password,
        },
    )


def iniciar_sesion(email, password="clave-segura-123"):
    respuesta = client.post("/token", data={"username": email, "password": password})
    assert respuesta.status_code == 200
    return {"Authorization": f"Bearer {respuesta.json()['access_token']}"}


def test_crud_de_usuario():
    limpiar_usuarios()

    try:
        respuesta = registrar_usuario("Ana", "García", "ana@example.com")
        assert respuesta.status_code == 200
        usuario = respuesta.json()
        assert usuario["email"] == "ana@example.com"
        assert "password_hash" not in usuario
        assert "password" not in usuario

        respuesta = registrar_usuario("Luis", "Pérez", "luis@example.com")
        assert respuesta.status_code == 200
        headers = iniciar_sesion("luis@example.com")

        usuario_id = usuario["id"]
        respuesta = client.get(f"/usuarios/{usuario_id}", headers=headers)
        assert respuesta.status_code == 200

        respuesta = client.put(
            f"/usuarios/{usuario_id}",
            json={
                "nombre": "Ana María",
                "apellido": "García",
                "email": "ana.maria@example.com",
            },
            headers=headers,
        )
        assert respuesta.status_code == 200
        assert respuesta.json()["nombre"] == "Ana María"

        respuesta = client.delete(f"/usuarios/{usuario_id}", headers=headers)
        assert respuesta.status_code == 200

        respuesta = client.get(f"/usuarios/{usuario_id}", headers=headers)
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
            "password": "clave-segura-123",
        }
        assert client.post("/usuarios/", json=usuario).status_code == 200
        respuesta = client.post("/usuarios/", json=usuario)
        assert respuesta.status_code == 400
    finally:
        limpiar_usuarios()


def test_rutas_protegidas_requieren_token():
    assert client.get("/usuarios/").status_code == 401


def test_login_rechaza_contrasena_incorrecta():
    limpiar_usuarios()

    try:
        assert registrar_usuario("Ana", "García", "ana@example.com").status_code == 200
        respuesta = client.post(
            "/token",
            data={"username": "ana@example.com", "password": "incorrecta"},
        )
        assert respuesta.status_code == 401
    finally:
        limpiar_usuarios()
