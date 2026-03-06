from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Project, Ticket, Comment, UserProfile


class ProjectModelTest(TestCase):
    # Tests that the Project model saves and returns data correctly

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123!')
        self.project = Project.objects.create(
            name='Test Project',
            description='A test project',
            owner=self.user
        )

    def test_project_str(self):
        # Tests that the __str__ method returns the project name
        self.assertEqual(str(self.project), 'Test Project')

    def test_project_creation(self):
        # Tests that project fields are saved correctly
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.owner, self.user)
        self.assertEqual(self.project.description, 'A test project')


class TicketModelTest(TestCase):
    # Tests that the Ticket model saves and returns data correctly

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.project = Project.objects.create(name='Test Project', owner=self.user)
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='A test ticket description',
            project=self.project,
            status='TO-DO',
            priority='MEDIUM',
            created_by=self.user,
            assigned_to=self.user
        )

    def test_ticket_str(self):
        # Tests that __str__ returns the ticket title
        self.assertEqual(str(self.ticket), 'Test Ticket')

    def test_ticket_default_status(self):
        # Tests that a new ticket defaults to TO-DO status
        new_ticket = Ticket.objects.create(
            title='Another Ticket',
            description='Description',
            project=self.project,
            created_by=self.user
        )
        self.assertEqual(new_ticket.status, 'TO-DO')

    def test_ticket_default_priority(self):
        # Tests that a new ticket defaults to MEDIUM priority
        new_ticket = Ticket.objects.create(
            title='Another Ticket',
            description='Description',
            project=self.project,
            created_by=self.user
        )
        self.assertEqual(new_ticket.priority, 'MEDIUM')
    
    def test_ticket_creation(self):
        # Tests that a ticket fields are saved correctly 
        self.assertEqual(self.ticket.title, 'Test Ticket')
        self.assertEqual(self.ticket.description, 'A test ticket description')
        self.assertEqual(self.ticket.project, self.project)
        self.assertEqual(self.ticket.status, 'TO-DO')
        self.assertEqual(self.ticket.priority, 'MEDIUM')
        self.assertEqual(self.ticket.created_by, self.user)
        self.assertEqual(self.ticket.assigned_to, self.user)

class CommentModelTest(TestCase):
    # Tests the Comment model

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.project = Project.objects.create(name='Test Project', owner=self.user)
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Description',
            project=self.project,
            created_by=self.user
        )
        self.comment = Comment.objects.create(
            ticket=self.ticket,
            author=self.user,
            text='This is a test comment'
        )

    def test_comment_str(self):
        # Tests that __str__ returns the first 30 characters of the comment
        self.assertEqual(str(self.comment), 'This is a test comment')

    def test_comment_linked_to_ticket(self):
        # Tests that the comment is correctly linked to its ticket
        self.assertEqual(self.comment.ticket, self.ticket)
        
    def test_comment_creation(self):
        # Tests that a ticket fields are saved correctly 
        self.assertEqual(self.comment.ticket, self.ticket)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.text, 'This is a test comment')

class UserProfileModelTest(TestCase):
    # Tests the UserProfile model

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.profile = UserProfile.objects.create(
            user=self.user,
            job_title='Developer',
            department='Engineering',
            location='London, UK'
        )

    def test_profile_str(self):
        # Tests that __str__ returns the username
        self.assertEqual(str(self.profile), 'testuser')

    def test_profile_linked_to_user(self):
        # Tests the OneToOne relationship between profile and user
        self.assertEqual(self.profile.user, self.user)
        
    def test_profile_creation(self):
        # Tests the Profile fields are saved correctly 
        self.assertEqual(self.profile.job_title, 'Developer')
        self.assertEqual(self.profile.department, 'Engineering')
        self.assertEqual(self.profile.location, 'London, UK')
        
class ViewAccessTest(TestCase):
    # Tests that views are accessible to the right users

    def setUp(self):
        # Creates a regular user and a staff user for testing
        self.client = Client()
        self.user = User.objects.create_user(username='regularuser', password='TestPass123!')
        self.staff_user = User.objects.create_user(username='staffuser', password='TestPass123!', is_staff=True)
        self.project = Project.objects.create(name='Test Project', owner=self.staff_user)
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Description',
            project=self.project,
            created_by=self.user
        )

    def test_home_redirects_when_not_logged_in(self):
        # Tests that unauthenticated users are redirected away from home
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 302)

    def test_home_accessible_when_logged_in(self):
        # Tests that authenticated users can access the home page
        self.client.login(username='regularuser', password='TestPass123!')
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_ticket_list_accessible_when_logged_in(self):
        # Tests that the ticket list page loads for authenticated users
        self.client.login(username='regularuser', password='TestPass123!')
        response = self.client.get(reverse('core:ticket_list'))
        self.assertEqual(response.status_code, 200)

    def test_delete_ticket_blocked_for_regular_user(self):
        # Tests that regular users cannot access the delete ticket URL
        self.client.login(username='regularuser', password='TestPass123!')
        response = self.client.post(reverse('core:delete_ticket', args=[self.ticket.pk]))
        # Should redirect away rather than deleting
        self.assertNotEqual(response.status_code, 200)

    def test_delete_ticket_allowed_for_staff(self):
        # Tests that staff users can delete tickets
        self.client.login(username='staffuser', password='TestPass123!')
        response = self.client.post(reverse('core:delete_ticket', args=[self.ticket.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ticket.objects.filter(pk=self.ticket.pk).exists())


class TicketFormTest(TestCase):
    # Tests form validation behaviour

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.project = Project.objects.create(name='Test Project', owner=self.user)

    def test_valid_ticket_form(self):
        # Tests that a fully filled form is valid
        from core.forms import TicketForm
        form = TicketForm(data={
            'title': 'Test Ticket',
            'description': 'A description',
            'project': self.project.pk,
            'status': 'TO-DO',
            'priority': 'MEDIUM',
            'assigned_to': ''
        })
        self.assertTrue(form.is_valid())

    def test_invalid_ticket_form_missing_title(self):
        # Tests that a form without a title fails validation
        from core.forms import TicketForm
        form = TicketForm(data={
            'title': '',
            'description': 'A description',
            'project': self.project.pk,
            'status': 'TO-DO',
            'priority': 'MEDIUM',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)