from django.test import TestCase
from django.urls import reverse
from .models import NutritionEntry, Food
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import Client

User = get_user_model()


class PERatioTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='foo')
        self.protein_food_1 = 5
        self.fat_food_1 = 8
        self.carb_food_1 = 12

        self.protein_food_2 = 18
        self.fat_food_2 = 4
        self.carb_food_2 = 0

        food1 = Food.objects.create(name='food1', protein_grams=self.protein_food_1,
                                    fat_grams=self.fat_food_1,
                                    carb_grams=self.carb_food_1, user=self.user)

        food2 = Food.objects.create(name='food2', protein_grams=self.protein_food_2,
                                    fat_grams=self.fat_food_2,
                                    carb_grams=self.carb_food_2, user=self.user)
        nut1 = NutritionEntry.objects.create(food=food1, date=timezone.now().date(), user=self.user)
        nut2 = NutritionEntry.objects.create(food=food2, date=timezone.now() - timezone.timedelta(days=1), user=self.user)
        nut3 = NutritionEntry.objects.create(food=food2, date=timezone.now().date(), user=self.user)

        self.client = Client()

    def test_all_data_for_today_in_context_and_no_other(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pe_ratio'))
        self.assertEqual(2, len(response.context['nutrition_entries']))

    def test_pe_ratio_correct(self):
        total_protein_for_day = self.protein_food_1 + self.protein_food_2
        total_carbs_for_day = self.carb_food_1 + self.carb_food_2
        total_fat_for_day = self.fat_food_1 + self.fat_food_2
        total_energy = total_carbs_for_day + total_fat_for_day
        pe_ratio = total_protein_for_day / total_energy

        self.client.force_login(self.user)
        response = self.client.get(reverse('pe_ratio'))
        self.assertEqual(pe_ratio, response.context['pe_ratio'])

    def test_redirect_to_login_if_not_logged_in(self):
        response = self.client.get(reverse('pe_ratio'))
        self.assertEqual(302, response.status_code)


class IndexTest(TestCase):

    def test_index_uses_correct_template_if_logged_in(self):
        pass

    def test_redirect_login(self):
        pass

    def test_route_directs_to_correct_view(self):
        pass
