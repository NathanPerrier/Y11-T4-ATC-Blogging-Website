from decimal import Decimal

from backend.tests.db import db, app
from backend.config import *

from mock import Mock, patch
from werkzeug.datastructures import Headers

from backend.tests.test_base import BaseTestCase
from backend.authentication.user import User
from backend.tracking.models import Site, Visit
from backend.hosting import views

class TrackingViewsTests(BaseTestCase):
    def test_visitors_location_is_derived_from_ip(self):
        with app.app_context():
            user = User.create(first_name='TEST', last_name="USER", email='alice@example.com', username=User().split_email('alice@example.com'), password='password', admin=User().is_admin('test', 'user', 'alice@example.com'))
            site = Site.create(user_id=user.id)

        mock_geodata = Mock(name='get_geodata')
        mock_geodata.return_value = {
            'city': 'Los Angeles',
            'zipcode': '90001',
            'latitude': '34.05',
            'longitude': '-118.25'
        }

        url = url_for('tracking.add_visit', site_id=site.id)
        wsgi_environment = {'REMOTE_ADDR': '1.2.3.4'}
        headers = Headers([('Referer', '/some/url')])

        with patch.object(views, 'get_geodata', mock_geodata):
            with self.client:
                self.client.get(url, environ_overrides=wsgi_environment,
                                headers=headers)

                visits = Visit.query_all()

                mock_geodata.assert_called_once_with('1.2.3.4')
                self.assertEqual(1, len(visits))

                first_visit = visits[0]
                self.assertEqual("/some/url", first_visit.url)
                self.assertEqual('Los Angeles, 90001', first_visit.location)
                self.assertEqual(Decimal("34.05"), first_visit.latitude)
                self.assertEqual(Decimal("-118.25"), first_visit.longitude)
    
    def test_attributes(self):
        # Checkpoint: Testing attributes of Site class
        site = Site()
        self.assertTrue(hasattr(site, 'id'))
        self.assertTrue(hasattr(site, 'base_url'))
        self.assertTrue(hasattr(site, 'visits'))
        self.assertTrue(hasattr(site, 'user_id'))

    def test_view_site_visits(self):
        # Create a test user
        with app.app_context():
            user = User.create(first_name='TEST', last_name="USER", email='alice2@example.com', username=User().split_email('alice2@example.com'), password='password', admin=User().is_admin('test', 'user', 'alice2@example.com'))
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        # Create a test site
        site = Site(name="Test Site", user_id=user.id)
        with app.app_context():
            db.session.add(site)
            db.session.commit()

        # Create a test visit
        visit = Visit(site_id=site.id, ip_address="127.0.0.1")
        with app.app_context():
            db.session.add(visit)
            db.session.commit()

        # Log in as the test user
        self.client.post("/login", data=dict(
            username="testuser",
            password="testpassword"
        ))

        # Test viewing the site visits
        response = self.client.get(url_for("tracking.view_site_visits", site_id=site.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Site", response.data)
        self.assertIn(b"127.0.0.1", response.data)