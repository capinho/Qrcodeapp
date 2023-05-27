from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from qrgen.models import QrCode, QrType, File
import os, shutil
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from qrgen.views import create_or_get_types
import tempfile


class GenerationDashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.generate_url = reverse("qrgen:generate")
        self.user_credentials = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )
        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )
        # Create QrType objects if they don't exist
        create_or_get_types()

    def tearDown(self):
        # Supprimer les fichiers temporaires créés pendant les tests
        folder_path = os.path.join(settings.BASE_DIR, "temp")
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    def test_generate_view_get(self):
        # Vérifier si la vue génère une réponse HTTP 200 pour une requête GET
        response = self.client.get(self.generate_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "qrgen/generation.html")

    def test_generate_view_post_url(self):
        # Vérifier si un QR code est généré avec succès lors d'une requête POST avec une URL
        form_data = {
            "generate": "true",
            "qrcode_type": "dynamic",
            "action_type": "url",
            "url": "https://example.com",
        }
        response = self.client.post(
            self.generate_url, form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 200)
        qrcode = QrCode.objects.last()
        self.assertEqual(qrcode.user, self.user)
        self.assertEqual(qrcode.type.name, "dynamic")
        self.assertEqual(qrcode.action_type, "url")
        self.assertEqual(qrcode.input_url, "https://example.com")
        # self.assertEqual(qrcode.action_url, "https://example.com")
        self.assertTrue(qrcode.is_dynamic)
        self.assertIsNotNone(qrcode.img)

    def test_generate_view_post_upload(self):
        # Vérifier si un QR code est généré avec succès lors d'une requête POST avec un fichier uploadé
        form_data = {
            "generate": "true",
            "qrcode_type": "static",
            "action_type": "pdf",
        }
        with open("media/user_files/Documents_scannes.pdf", "rb") as file:
            form_data["upload_file"] = file
            response = self.client.post(
                self.generate_url, form_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
            )
        self.assertEqual(response.status_code, 200)
        qrcode = QrCode.objects.last()
        self.assertEqual(qrcode.user, self.user)
        self.assertEqual(qrcode.type.name, "static")
        self.assertEqual(qrcode.action_type, "pdf")
        self.assertIsNone(qrcode.input_url)
        self.assertIsNotNone(qrcode.file)
        self.assertEqual(qrcode.file.name, "Documents_scannes.pdf")
        # self.assertTrue(qrcode.file.url.startswith("/media/user_files/"))
        # self.assertTrue(qrcode.file.url.endswith("/test.pdf"))
        self.assertEqual(
            qrcode.action_url, f"http://testserver/qrcode/download/{qrcode.file.id}"
        )
        self.assertFalse(qrcode.is_dynamic)
        self.assertIsNotNone(qrcode.img)


class MainDashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse("qrgen:dashboard")
        self.user_credentials = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )
        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )

    def test_dashboard_view_get(self):
        # Vérifier si la vue génère une réponse HTTP 200 pour une requête GET
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "qrgen/dashboard.html")


class EditQrCodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.edit_url = reverse("qrgen:edit_qrcode", args=[1])
        self.user_credentials = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )
        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )

    def test_edit_view_post_change_content_url(self):
        # Vérifier si le contenu d'un QR code est modifié avec succès lors d'une requête POST avec une URL
        # Create a temporary image file for testing
        with open("media/qrcodes/qrcode-1.png", "rb") as f:
            image_content = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )
        create_or_get_types()
        qr_type = QrType.objects.get(name="dynamic")

        qrcode = QrCode.objects.create(
            user=self.user,
            input_url="https://example.com",
            type=qr_type,
            img=image_file,
        )
        form_data = {
            "change_content": "true",
            "new_content": "https://newexample.com",
        }
        response = self.client.post(self.edit_url, form_data)
        self.assertRedirects(response, reverse("qrgen:dashboard"))
        qrcode.refresh_from_db()
        self.assertEqual(qrcode.input_url, "https://newexample.com")

    def test_edit_view_post_change_content_file(self):
        # Vérifier si le contenu d'un QR code est modifié avec succès lors d'une requête POST avec un fichier uploadé

        # Create a temporary image file for testing
        with open("media/qrcodes/qrcode-1.png", "rb") as f:
            image_content = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )

        create_or_get_types()
        qr_type = QrType.objects.get(name="dynamic")

        qrcode = QrCode.objects.create(user=self.user, type=qr_type, img=image_file)
        form_data = {
            "change_content": "true",
        }
        # Créer un fichier temporaire pour les tests
        file_content = b"File content"  # Remplacez cela par le contenu réel du fichier
        uploaded_file = SimpleUploadedFile(
            "new_file.pdf", file_content, content_type="application/pdf"
        )
        form_data["new_file"] = uploaded_file
        response = self.client.post(self.edit_url, form_data)

        self.assertRedirects(response, reverse("qrgen:dashboard"))
        qrcode.refresh_from_db()
        self.assertIsNotNone(qrcode.file)
        self.assertEqual(qrcode.file.name, "new_file.pdf")
        # self.assertTrue(os.path.exists(qrcode.file.path))

    # def test_edit_view_post_change_title(self):
    #     # Vérifier si le titre d'un QR code est modifié avec succès lors d'une requête POST
    #     qrcode = QrCode.objects.create(user=self.user, title="Old Title")
    #     form_data = {
    #         "change_title": "true",
    #         "new_title": "New Title",
    #     }
    #     response = self.client.post(self.edit_url, form_data)
    #     self.assertRedirects(response, reverse("qrgen:dashboard"))
    #     qrcode.refresh_from_db()
    #     self.assertEqual(qrcode.title, "New Title")


class DeleteQrCodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.delete_url = reverse("qrgen:delete_qrcode", args=[1])
        self.user_credentials = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )
        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )

    def test_delete_view_get(self):
        # Créer un objet QrCode pour effectuer la suppression
        qrcode = QrCode.objects.create(user=self.user, type_id=1)

        # Mettre à jour l'URL de suppression en utilisant l'ID de qrcode créé
        delete_url = reverse("qrgen:delete_qrcode", args=[qrcode.id])

        # Vérifier si la vue redirige vers le tableau de bord lors d'une requête GET
        response = self.client.get(delete_url)
        self.assertRedirects(response, reverse("qrgen:dashboard"))

        # Vérifier que le QR code a été supprimé
        self.assertFalse(QrCode.objects.filter(id=qrcode.id).exists())

    def test_delete_view_post(self):
        # Create a temporary image file for testing
        with open("media/qrcodes/qrcode-1.png", "rb") as f:
            image_content = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )
        create_or_get_types()
        qr_type = QrType.objects.get(name="dynamic")

        # Create a QrCode object with the temporary image file
        qrcode = QrCode.objects.create(user=self.user, type=qr_type, img=image_file)

        # Mettre à jour l'URL de suppression en utilisant l'ID de qrcode créé
        self.delete_url = reverse("qrgen:delete_qrcode", args=[qrcode.id])
        # Perform the delete request
        response = self.client.post(self.delete_url)
        # Assertions
        self.assertRedirects(response, reverse("qrgen:dashboard"))


class DownloadQrCodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.download_url = reverse("qrgen:download_qrcode", args=[1, "pdf"])
        self.user_credentials = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )
        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )

    def test_download_view(self):
        # Create a temporary image file for testing
        with open("media/qrcodes/qrcode-1.png", "rb") as f:
            image_content = f.read()
        image_file = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )
        create_or_get_types()
        qr_type = QrType.objects.get(name="dynamic")

        # Create a QrCode object with the temporary image file
        qrcode = QrCode.objects.create(
            user=self.user,
            title="Test QR Code",
            type=qr_type,
            img=image_file,
        )

        # Set up the temporary image file locally
        temp_image_path = "temp/qrcodes/1/Test QR Code.png"
        os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)
        with open(temp_image_path, "wb") as f:
            f.write(image_content)

        # Perform the download request
        response = self.client.get(self.download_url)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/adminupload")
