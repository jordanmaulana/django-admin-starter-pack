from django.test import TestCase

from api.v1.serializers.calculation_serializer import CalculationSerializer
from apps.calculations.consts import ROOF_SHAPE_LIMASAN
from apps.calculations.models import Calculation


class CalculationSerializerTest(TestCase):
    def setUp(self):
        self.calculation = Calculation.objects.create(
            shape=ROOF_SHAPE_LIMASAN,
            lebar=10,
            panjang=10,
            overhang=1,
            tilt=30,
        )

    def test_serializer_contains_expected_fields(self):
        serializer = CalculationSerializer(instance=self.calculation)
        data = serializer.data
        self.assertEqual(data["luas_atap_datar"], 144.0)
        self.assertAlmostEqual(data["luas_atap_miring"], 166.0, places=3)
        self.assertEqual(data["panjang_jurai"], 7.64)
        self.assertEqual(data["panjang_nok"], 30.56)
        self.assertEqual(data["panjang_overhang"], 12.0)
        self.assertEqual(data["lebar_overhang"], 12.0)
