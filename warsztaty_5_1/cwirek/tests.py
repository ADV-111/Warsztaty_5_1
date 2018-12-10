from django.contrib.auth.forms import PasswordChangeForm
from django.test import TestCase

from .forms import TweetForm, CommentForm, MessageForm, UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from .models import Tweet, User, Comments, Messages
from django.urls import reverse


class CwirekTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.com', password='12345')
        login = self.client.login(email='testuser@mail.com', password='12345')

# models
    def create_tweet(self):
        content = "Przykladowy content"
        deleted = False
        return Tweet.objects.create(content=content, user=self.user, deleted=deleted)

    def test_tweet_creation(self):
        t = self.create_tweet()
        self.assertTrue(isinstance(t, Tweet))
        self.assertFalse(t.deleted)
        self.assertEqual(t.__str__(), 'testuser@mail.com >>> Przykladowy content')

    def create_comment(self):
        content = "Przykladowy komentarz"
        tweet = self.create_tweet()
        return Comments.objects.create(content=content, tweet=tweet, user=self.user)

    def test_comment_creation(self):
        c = self.create_comment()
        should_get = 'testuser@mail.com - testuser@mail.com >>> Przykladowy content >>> Przykladowy komentarz'
        self.assertTrue(isinstance(c, Comments))
        self.assertFalse(c.deleted)
        self.assertEqual(c.__str__(), should_get)

    def create_user_message_to(self):
        self.user = User.objects.create_user(email='testuser2@mail.com', password='12345')
        login = self.client.login(email='testuser2@mail.com', password='12345')
        return self.user

    def create_message(self):
        content = 'Przykladowa wiadomosc'
        send_to = self.user
        send_from = self.create_user_message_to()
        return Messages.objects.create(content=content, send_to=send_to, send_from=send_from)

    def test_created_message(self):
        m = self.create_message()
        should_get = 'testuser2@mail.com - testuser@mail.com >>> Przykladowa wiadomosc'
        self.assertTrue(isinstance(m, Messages))
        self.assertFalse(m.read)
        self.assertFalse(m.deleted)
        self.assertEqual(m.__str__(), should_get)

# views
    def test_home_view(self):
        t = self.create_tweet()
        url = reverse("main")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(t.content, resp.content.decode())
        self.assertTemplateUsed(resp, 'cwirek/main.html')

    def test_tweet_create_view(self):
        url = reverse("tweet-add")
        resp = self.client.get(url)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/tweet_form.html')
        self.assertIsInstance(form, TweetForm)
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_tweet_detail_view(self):
        t = self.create_tweet()
        url = reverse('tweet-detail', kwargs={'pk': t.id})
        resp = self.client.get(url)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/tweet_detail.html')
        self.assertIn(t.content, resp.content.decode())
        self.assertIsInstance(form, CommentForm)
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_tweet_delete_view(self):
        t = self.create_tweet()
        url = reverse('tweet-delete', kwargs={'pk': t.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/tweet_confirm_delete.html')
        self.assertContains(resp, 'csrfmiddlewaretoken')
        self.assertContains(resp, 'type="submit"', 1)

    def test_user_self_tweets_view(self):
        t = self.create_tweet()
        url = reverse('user-tweets', kwargs={'id_user': self.user.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(t.content, resp.content.decode())
        self.assertTemplateUsed(resp, 'cwirek/user_tweets.html')
        self.assertNotContains(resp, 'Wyślij wiadomość')

    def test_user_another_one_tweets_view(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        t = Tweet.objects.create(content="Przykladowy content", user=user1)
        url = reverse('user-tweets', kwargs={'id_user': user1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(t.content, resp.content.decode())
        self.assertTemplateUsed(resp, 'cwirek/user_tweets.html')
        self.assertContains(resp, 'Wyślij wiadomość', 1)

    def test_message_user_self_view(self):
        url = reverse('user-message', kwargs={'id_user': self.user.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_message_user_another_view(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        url = reverse('user-message', kwargs={'id_user': user1.id})
        resp = self.client.get(url)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)
        self.assertIn(user1.email, resp.content.decode())
        self.assertTemplateUsed(resp, 'cwirek/message_form.html')
        self.assertContains(resp, 'csrfmiddlewaretoken')
        self.assertContains(resp, 'type="submit"', 1)
        self.assertEqual(form, MessageForm)

    def test_all_messages_view(self):
        url = reverse('user-messages')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/user_messages.html')
        self.assertContains(resp, '/user_sent_messages/', 1)
        self.assertContains(resp, '/user_received_messages/', 1)

    def test_user_received_messages(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        m = Messages.objects.create(content="Content", send_to=self.user, send_from=user1)
        url = reverse('user-received-messages')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/user_messages_received.html')
        self.assertIn(m.content, resp.content.decode())
        self.assertContains(resp, '/user_sent_messages/', 1)
        self.assertContains(resp, '/user_received_messages/', 2)
        self.assertContains(resp, 'Wyślij wiadomość', 1)
        self.assertFalse(m.read)

    def test_user_sent_messages(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        m = Messages.objects.create(content="Content", send_from=self.user, send_to=user1)
        url = reverse('user-sent-messages')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/user_messages_sent.html')
        self.assertIn(m.content, resp.content.decode())
        self.assertContains(resp, '/user_sent_messages/', 2)
        self.assertContains(resp, '/user_received_messages/', 1)
        self.assertFalse(m.read)

    def test_message_received_specific_view(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        m = Messages.objects.create(content="Content", send_to=self.user, send_from=user1)
        url = reverse('user-message-received-specific', kwargs={'id_message': m.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/message_detail.html')
        self.assertIn(m.content, resp.content.decode())
        self.assertContains(resp, 'Wyślij wiadomość', 1)

    def test_message_sent_specific_view(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        m = Messages.objects.create(content="Content", send_from=self.user, send_to=user1)
        url = reverse('user-message-sent-specific', kwargs={'id_message': m.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/message_detail.html')
        self.assertIn(m.content, resp.content.decode())
        self.assertFalse(m.read)

    def test_profile_view(self):
        url = reverse('profile')
        resp = self.client.get(url)
        form1 = resp.context['u_form']
        form2 = resp.context['p_form']
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/profile.html')
        self.assertContains(resp, 'csrfmiddlewaretoken')
        self.assertContains(resp, 'type="submit"', 3)
        self.assertIsInstance(form1, UserUpdateForm)
        self.assertIsInstance(form2, ProfileUpdateForm)

    def test_change_password_view(self):
        url = reverse('change-password')
        resp = self.client.get(url)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/user_confirm_password_change.html')
        self.assertContains(resp, 'csrfmiddlewaretoken')
        self.assertContains(resp, 'type="submit"', 1)
        self.assertIsInstance(form, PasswordChangeForm)

    def test_delete_user_view(self):
        url = reverse('delete-user', kwargs={'pk': self.user.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/user_confirm_delete.html')
        self.assertContains(resp, 'csrfmiddlewaretoken')
        self.assertContains(resp, 'type="submit"', 1)
        self.assertContains(resp, '/profile/', 2)

    def test_login_when_loggedin_view(self):
        url = reverse('login')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

    def test_register_when_loggedin_view(self):
        url = reverse('register')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

    def test_logout_view(self):
        url = reverse('logout')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/logout.html')

    def tearDown(self):
        self.user = None


class LoggedOutTest(TestCase):
    def test_home_view_logged_out(self):
        url = reverse("main")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/')

    def test_tweet_create_view_logged_out(self):
        url = reverse("tweet-add")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/add_tweet/')

    def test_tweet_detail_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        content = "Przykladowy content"
        t = Tweet.objects.create(content=content, user=user1)
        url = reverse('tweet-detail', kwargs={'pk': t.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/tweet/{t.id}/')

    def test_tweet_delete_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        content = "Przykladowy content"
        t = Tweet.objects.create(content=content, user=user1)
        url = reverse('tweet-delete', kwargs={'pk': t.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/tweet_delete/{t.id}/')

    def test_user_self_tweets_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        url = reverse('user-tweets', kwargs={'id_user': user1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/user_tweets/{user1.id}/')

    def test_user_another_one_tweets_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        t = Tweet.objects.create(content="Przykladowy content", user=user1)
        url = reverse('user-tweets', kwargs={'id_user': user1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/user_tweets/{user1.id}/')

    def test_message_user_self_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        url = reverse('user-message', kwargs={'id_user': user1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/user_message/{user1.id}/')

    def test_message_user_another_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        url = reverse('user-message', kwargs={'id_user': user1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/user_message/{user1.id}/')

    def test_all_messages_view_logged_out(self):
        url = reverse('user-messages')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/user_messages/')

    def test_user_received_messages_logged_out(self):
        url = reverse('user-received-messages')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/user_received_messages/')

    def test_user_sent_messages_logged_out(self):
        url = reverse('user-sent-messages')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/user_sent_messages/')

    def test_message_received_specific_view(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        user2 = User.objects.create_user(email='testuser3@mail.com', password='12345')
        m = Messages.objects.create(content="Content", send_to=user2, send_from=user1)
        url = reverse('user-message-received-specific', kwargs={'id_message': m.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/user_received_messages/{m.id}/')

    def test_message_sent_specific_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        user2 = User.objects.create_user(email='testuser3@mail.com', password='12345')
        m = Messages.objects.create(content="Content", send_from=user2, send_to=user1)
        url = reverse('user-message-sent-specific', kwargs={'id_message': m.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/user_sent_messages/{m.id}/')

    def test_profile_view_logged_out(self):
        url = reverse('profile')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/profile/')

    def test_change_password_view_logged_out(self):
        url = reverse('change-password')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/change_password/')

    def test_delete_user_view_logged_out(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        url = reverse('delete-user', kwargs={'pk': user1.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/login/?next=/delete_user/{user1.id}/')

    def test_login_view_logged_out(self):
        url = reverse('login')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/login.html')
        self.assertContains(resp, 'csrfmiddlewaretoken')
        self.assertContains(resp, 'type="submit"', 1)

    def test_register_view_logged_out(self):
        url = reverse('register')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cwirek/register.html')
        self.assertContains(resp, 'csrfmiddlewaretoken')
        self.assertContains(resp, 'type="submit"', 1)

    def test_logout_view_logged_out(self):
        url = reverse('logout')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class FormTest(TestCase):

    def test_valid_tweet_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        t = Tweet.objects.create(content="Przykladowy content", user=user1)
        data = {'content': t.content}
        form = TweetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_tweet_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        content = ""
        t = Tweet.objects.create(content=content, user=user1)
        data = {'content': t.content}
        form = TweetForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_comment_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        t = Tweet.objects.create(content="Przykladowy content", user=user1)
        m = Comments.objects.create(content="Przykladowy content", user=user1, tweet=t)
        data = {'content': t.content}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        t = Tweet.objects.create(content="Przykladowy content", user=user1)
        m = Comments.objects.create(content="", user=user1, tweet=t)
        data = {'content': m.content}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_message_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        user2 = User.objects.create_user(email='testuser3@mail.com', password='12345')
        m = Messages.objects.create(content="Przykladowy conent", send_to=user1, send_from=user2)
        data = {'content': m.content}
        form = MessageForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_message_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345')
        user2 = User.objects.create_user(email='testuser3@mail.com', password='12345')
        m = Messages.objects.create(content="", send_to=user1, send_from=user2)
        data = {'content': m.content}
        form = MessageForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_user_register_form(self):
        data = {'email': 'testuser15@mail.com', 'password1': 'nowehaslo15', 'password2': 'nowehaslo15',
                'first_name': 'aaba', 'last_name': 'dsaba'}
        form = UserRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_register_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345', first_name='aaa', last_name='bbb')
        data = {'email': user1.email, 'password1': user1.password, 'password2': '54321',
                'first_name': user1.first_name, 'last_name': user1.last_name}
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_user_update_form(self):
        user1 = User.objects.create_user(email='testuser2@mail.com', password='12345', first_name='aaa', last_name='bbb')
        data = {'first_name': user1.first_name, 'last_name': user1.last_name}
        form = UserUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_update_form(self):
        first_name = 'aaadsafsgfdhfdshgfhjgfjgfjgjghfdhgfkhgdfhgfkhgdfhgfdhjgfkjgfhgfkgfddhgfdhgfdhgfddhgfdhdg'
        last_name = ''
        data = {'first_name': first_name, 'last_name': last_name}
        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
