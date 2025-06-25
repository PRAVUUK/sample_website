from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, datetime
from tasks.models import (Task, TaskCategory, TaskPriority, TaskReminder, 
                         TaskComment, TaskTimeLog, TaskTemplate, TaskBoard, TaskStatistics)
from tasks.forms import TaskForm, TaskCategoryForm

User = get_user_model()


class TaskModelTest(TestCase):
    """Test cases for Task model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.priority = TaskPriority.objects.create(
            name='High',
            level=3,
            color='#dc3545'
        )
        self.category = TaskCategory.objects.create(
            name='Work',
            user=self.user,
            color='#007bff'
        )
    
    def test_create_task(self):
        """Test task creation"""
        task = Task.objects.create(
            title='Test Task',
            description='Test description',
            user=self.user,
            category=self.category,
            priority=self.priority,
            due_date=timezone.now() + timedelta(days=1)
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.status, 'pending')
        self.assertEqual(task.progress, 0)
    
    def test_task_str_representation(self):
        """Test task string representation"""
        task = Task.objects.create(
            title='Test Task',
            user=self.user
        )
        self.assertEqual(str(task), 'Test Task')
    
    def test_task_completion(self):
        """Test task completion functionality"""
        task = Task.objects.create(
            title='Test Task',
            user=self.user
        )
        task.mark_completed()
        self.assertEqual(task.status, 'completed')
        self.assertEqual(task.progress, 100)
        self.assertIsNotNone(task.completed_at)
    
    def test_task_is_overdue(self):
        """Test task overdue property"""
        # Future task
        future_task = Task.objects.create(
            title='Future Task',
            user=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(future_task.is_overdue)
        
        # Past task
        past_task = Task.objects.create(
            title='Past Task',
            user=self.user,
            due_date=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(past_task.is_overdue)
        
        # Completed past task
        completed_task = Task.objects.create(
            title='Completed Task',
            user=self.user,
            due_date=timezone.now() - timedelta(days=1),
            status='completed'
        )
        self.assertFalse(completed_task.is_overdue)
    
    def test_task_time_remaining(self):
        """Test task time remaining property"""
        future_task = Task.objects.create(
            title='Future Task',
            user=self.user,
            due_date=timezone.now() + timedelta(hours=2)
        )
        time_remaining = future_task.time_remaining
        self.assertIsNotNone(time_remaining)
        self.assertGreater(time_remaining.total_seconds(), 0)


class TaskCategoryTest(TestCase):
    """Test cases for TaskCategory model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_category(self):
        """Test category creation"""
        category = TaskCategory.objects.create(
            name='Work',
            user=self.user,
            color='#007bff',
            description='Work related tasks'
        )
        self.assertEqual(category.name, 'Work')
        self.assertEqual(category.user, self.user)
        self.assertTrue(category.is_active)
    
    def test_category_str_representation(self):
        """Test category string representation"""
        category = TaskCategory.objects.create(
            name='Work',
            user=self.user
        )
        self.assertEqual(str(category), 'Work')
    
    def test_category_task_count(self):
        """Test category task count property"""
        category = TaskCategory.objects.create(
            name='Work',
            user=self.user
        )
        
        # Create tasks
        Task.objects.create(title='Task 1', user=self.user, category=category)
        Task.objects.create(title='Task 2', user=self.user, category=category)
        Task.objects.create(title='Deleted Task', user=self.user, category=category, is_deleted=True)
        
        self.assertEqual(category.task_count, 2)


class TaskPriorityTest(TestCase):
    """Test cases for TaskPriority model"""
    
    def test_create_priority(self):
        """Test priority creation"""
        priority = TaskPriority.objects.create(
            name='High',
            level=3,
            color='#dc3545',
            description='High priority tasks'
        )
        self.assertEqual(priority.name, 'High')
        self.assertEqual(priority.level, 3)
    
    def test_priority_ordering(self):
        """Test priority ordering"""
        high = TaskPriority.objects.create(name='High', level=3, color='#dc3545')
        low = TaskPriority.objects.create(name='Low', level=1, color='#28a745')
        medium = TaskPriority.objects.create(name='Medium', level=2, color='#ffc107')
        
        priorities = list(TaskPriority.objects.all())
        self.assertEqual(priorities[0], low)
        self.assertEqual(priorities[1], medium)
        self.assertEqual(priorities[2], high)


class TaskFormTest(TestCase):
    """Test cases for TaskForm"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.priority = TaskPriority.objects.create(
            name='High',
            level=3,
            color='#dc3545'
        )
        self.category = TaskCategory.objects.create(
            name='Work',
            user=self.user,
            color='#007bff'
        )
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'category': self.category.id,
            'priority': self.priority.id,
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M'),
            'estimated_hours': 2.5
        }
        form = TaskForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
    
    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'category': self.category.id,
            'priority': self.priority.id,
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M'),
            'estimated_hours': 2.5
        }
        form = TaskForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        
        task = form.save(commit=False)
        task.user = self.user
        task.save()
        
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user, self.user)


class TaskViewsTest(TestCase):
    """Test cases for task views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.priority = TaskPriority.objects.create(
            name='High',
            level=3,
            color='#dc3545'
        )
        self.category = TaskCategory.objects.create(
            name='Work',
            user=self.user,
            color='#007bff'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_task_dashboard_view(self):
        """Test task dashboard view"""
        response = self.client.get(reverse('tasks:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task Dashboard')
    
    def test_task_list_view(self):
        """Test task list view"""
        # Create test tasks
        Task.objects.create(title='Task 1', user=self.user)
        Task.objects.create(title='Task 2', user=self.user)
        
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
    
    def test_create_task_view_get(self):
        """Test create task view GET request"""
        response = self.client.get(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Task')
    
    def test_create_task_view_post(self):
        """Test create task view POST request"""
        response = self.client.post(reverse('tasks:create_task'), {
            'title': 'New Task',
            'description': 'New task description',
            'category': self.category.id,
            'priority': self.priority.id,
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M'),
            'estimated_hours': 2
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())
    
    def test_task_detail_view(self):
        """Test task detail view"""
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            category=self.category
        )
        response = self.client.get(reverse('tasks:task_detail', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
    
    def test_edit_task_view(self):
        """Test edit task view"""
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            category=self.category
        )
        response = self.client.post(reverse('tasks:edit_task', args=[task.id]), {
            'title': 'Updated Task',
            'description': 'Updated description',
            'category': self.category.id,
            'priority': self.priority.id,
            'estimated_hours': 3
        })
        self.assertEqual(response.status_code, 302)
        
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
    
    def test_delete_task_view(self):
        """Test delete task view"""
        task = Task.objects.create(
            title='Test Task',
            user=self.user
        )
        response = self.client.post(reverse('tasks:delete_task', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        
        task.refresh_from_db()
        self.assertTrue(task.is_deleted)
    
    def test_task_calendar_view(self):
        """Test task calendar view"""
        response = self.client.get(reverse('tasks:task_calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Calendar')
    
    def test_task_board_view(self):
        """Test task board view"""
        response = self.client.get(reverse('tasks:task_board'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Board')


class TaskAjaxViewsTest(TestCase):
    """Test cases for task AJAX views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            user=self.user
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_update_task_status(self):
        """Test update task status AJAX endpoint"""
        response = self.client.post(reverse('tasks:update_task_status'), {
            'task_id': self.task.id,
            'status': 'completed'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')
    
    def test_toggle_task_importance(self):
        """Test toggle task importance AJAX endpoint"""
        response = self.client.post(reverse('tasks:toggle_task_importance'), {
            'task_id': self.task.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_important)
    
    def test_update_task_progress(self):
        """Test update task progress AJAX endpoint"""
        response = self.client.post(reverse('tasks:update_task_progress'), {
            'task_id': self.task.id,
            'progress': 50
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.progress, 50)


class TaskReminderTest(TestCase):
    """Test cases for TaskReminder model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            user=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )
    
    def test_create_reminder(self):
        """Test reminder creation"""
        reminder = TaskReminder.objects.create(
            task=self.task,
            user=self.user,
            reminder_type='email',
            timing='1_hour_before'
        )
        self.assertEqual(reminder.task, self.task)
        self.assertEqual(reminder.reminder_type, 'email')
        self.assertFalse(reminder.is_sent)


class TaskCommentTest(TestCase):
    """Test cases for TaskComment model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            user=self.user
        )
    
    def test_create_comment(self):
        """Test comment creation"""
        comment = TaskComment.objects.create(
            task=self.task,
            user=self.user,
            content='Test comment'
        )
        self.assertEqual(comment.task, self.task)
        self.assertEqual(comment.content, 'Test comment')


class TaskTimeLogTest(TestCase):
    """Test cases for TaskTimeLog model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            user=self.user
        )
    
    def test_create_time_log(self):
        """Test time log creation"""
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=2)
        
        time_log = TaskTimeLog.objects.create(
            task=self.task,
            user=self.user,
            start_time=start_time,
            end_time=end_time
        )
        self.assertEqual(time_log.task, self.task)
        self.assertIsNotNone(time_log.duration)
    
    def test_manual_time_log(self):
        """Test manual time log creation"""
        time_log = TaskTimeLog.objects.create(
            task=self.task,
            user=self.user,
            manual_hours=2.5,
            is_manual=True,
            description='Manual time entry'
        )
        self.assertTrue(time_log.is_manual)
        self.assertEqual(time_log.manual_hours, 2.5)


class TaskIntegrationTest(TestCase):
    """Integration tests for tasks module"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.priority = TaskPriority.objects.create(
            name='High',
            level=3,
            color='#dc3545'
        )
        self.category = TaskCategory.objects.create(
            name='Work',
            user=self.user,
            color='#007bff'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_complete_task_workflow(self):
        """Test complete task management workflow"""
        # Create task
        response = self.client.post(reverse('tasks:create_task'), {
            'title': 'Workflow Task',
            'description': 'Test workflow',
            'category': self.category.id,
            'priority': self.priority.id,
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M'),
            'estimated_hours': 3
        })
        self.assertEqual(response.status_code, 302)
        
        task = Task.objects.get(title='Workflow Task')
        
        # View task detail
        response = self.client.get(reverse('tasks:task_detail', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        
        # Update task progress
        response = self.client.post(reverse('tasks:update_task_progress'), {
            'task_id': task.id,
            'progress': 50
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        task.refresh_from_db()
        self.assertEqual(task.progress, 50)
        
        # Add comment
        response = self.client.post(reverse('tasks:add_task_comment'), {
            'task_id': task.id,
            'content': 'Progress update'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(TaskComment.objects.filter(
            task=task,
            content='Progress update'
        ).exists())
        
        # Mark as completed
        response = self.client.post(reverse('tasks:update_task_status'), {
            'task_id': task.id,
            'status': 'completed'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')
        self.assertEqual(task.progress, 100)
        self.assertIsNotNone(task.completed_at)
        
        # Verify task appears in completed list
        response = self.client.get(reverse('tasks:task_list') + '?status=completed')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Workflow Task')

