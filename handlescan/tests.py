import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from qrgen.models import QrCode, File, QrType
from qrgen.views import create_or_get_types


class QrCodeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Create QrType objects if they don't exist
        create_or_get_types()
        # create file
        self.file = File.objects.create(
            id=1,
            user=self.user,
            file=SimpleUploadedFile(
                "test_file.pdf", b"file_content", content_type="pdf"
            ),
        )
        qr_type = QrType.objects.get(
            name="dynamic"
        )  # Get the QrType object for "dynamic" code

        self.qrcode = QrCode.objects.create(
            id=1,
            user=self.user,
            scan_count=0,
            action_type="web",  # Choose 'web' for website URL
            input_url="https://example.com",
            type=qr_type,  # Set the type object directly
            file_id=1,
        )

    def test_dynamic_code_scan_view_redirect(self):
        # Vérifie si le scan d'un code QR dynamique avec l'action "web" redirige vers l'URL d'entrée attendue
        response = self.client.get(reverse("handlescan:dynamic", args=[self.qrcode.id]))
        self.assertEqual(response.status_code, 302)  # Assert the response is a redirect
        self.assertEqual(
            response.url, self.qrcode.input_url
        )  # Assert the redirect URL matches the expected input_url

    def test_dynamic_code_scan_view_email(self):
        # Vérifie si le scan d'un code QR dynamique avec l'action "eml" rend le modèle "email.html" avec l'adresse e-mail d'entrée
        self.qrcode.action_type = "eml"
        self.qrcode.input_url = "test@example.com"
        self.qrcode.save()

        response = self.client.get(reverse("handlescan:dynamic", args=[self.qrcode.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "email.html")

    def test_dynamic_code_scan_view_upload(self):
        # Vérifie si le scan d'un code QR dynamique avec l'action "pdf" redirige vers la vue de téléchargement correspondante
        self.qrcode.action_type = "pdf"
        self.qrcode.file = self.file
        self.qrcode.save()

        response = self.client.get(reverse("handlescan:dynamic", args=[self.qrcode.id]))
        self.assertEqual(response.status_code, 302)  # Assuming you expect a redirect
        expected_url = reverse("handlescan:download", args=[self.qrcode.file_id])
        self.assertEqual(response.url, expected_url)

    def test_download_view(self):
        # Vérifie si la vue de téléchargement renvoie le fichier attendu avec les en-têtes appropriés
        response = self.client.get(reverse("handlescan:download", args=[self.file.id]))
        self.assertEqual(response.status_code, 200)
        expected_filename = os.path.basename(self.file.file.name)
        self.assertEqual(
            response["Content-Disposition"], f"inline; filename={expected_filename}"
        )  # Vérifie le nom de fichier dans l'en-tête Content-Disposition

        # Vérifie que le contenu du fichier téléchargé est correct
        self.assertEqual(response.content, b"file_content")

    def test_download_view_invalid_file_id(self):
        # Vérifie si la vue de téléchargement renvoie une erreur File.DoesNotExist pour un ID de fichier invalide
        with self.assertRaises(File.DoesNotExist):
            response = self.client.get(reverse("handlescan:download", args=[999]))

    def test_dynamic_code_scan_view_invalid_qrcode_id(self):
        # Vérifie si la vue de scan dynamique renvoie une erreur QrCode.DoesNotExist pour un ID de code QR invalide
        with self.assertRaises(QrCode.DoesNotExist):
            response = self.client.get(reverse("handlescan:dynamic", args=[999]))

    def test_dynamic_code_scan_view_increment_scan_count(self):
        # Vérifie si le compteur de scans du code QR est incrémenté après le scan
        initial_scan_count = self.qrcode.scan_count
        self.client.get(reverse("handlescan:dynamic", args=[self.qrcode.id]))
        self.qrcode.refresh_from_db()
        self.assertEqual(self.qrcode.scan_count, initial_scan_count + 1)


class QrCodeViewsHttp404TestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dynamic_code_scan_view_qrcode_not_found(self):
        # Vérifie si la vue de scan dynamique renvoie une erreur QrCode.DoesNotExist pour un code QR non trouvé
        with self.assertRaises(QrCode.DoesNotExist):
            self.client.get(reverse("handlescan:dynamic", args=[1]))


class FileDownloadViewsHttp404TestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_download_view_file_not_found(self):
        # Vérifie si la vue de téléchargement renvoie une erreur File.DoesNotExist pour un fichier non trouvé
        with self.assertRaises(File.DoesNotExist):
            self.client.get(reverse("handlescan:download", args=[1]))
