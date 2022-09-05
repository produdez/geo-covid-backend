from djongo import models

class State(models.Model):
    initials = models.CharField(max_length=2, unique=True)
    name = models.TextField(unique=True)
class Report(models.Model):
    class Meta:
        unique_together = (('date','state'))
        indexes = [
            models.Index(fields=['date']),
        ]
        ordering = ['date']

    date = models.DateTimeField()
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING) # NOTE: state have index by default being a ForeignKey (https://stackoverflow.com/questions/5984842/does-django-automatically-generate-indexes-for-foreign-keys-columns)

    # TODO: Check data to find exact meaning of confirm, increase, cumulative and update serializer! TAG: thi
    # stats
    death = models.IntegerField(blank=True)
    death_confirmed = models.IntegerField(blank=True)
    death_increase = models.IntegerField(blank=True)
    death_probable = models.IntegerField(blank=True)
    hospitalized = models.IntegerField(blank=True)
    hospitalized_cumulative = models.IntegerField(blank=True)
    hospitalized_currently = models.IntegerField(blank=True)
    hospitalized_increase = models.IntegerField(blank=True)
    in_icu_cumulative = models.IntegerField(blank=True)
    in_icu_currently = models.IntegerField(blank=True)
    negative = models.IntegerField(blank=True)
    negative_increase = models.IntegerField(blank=True)
    negative_tests_antibody = models.IntegerField(blank=True)
    negative_tests_people_antibody = models.IntegerField(blank=True)
    negative_tests_viral = models.IntegerField(blank=True)
    on_ventilator_cumulative = models.IntegerField(blank=True)
    on_ventilator_currently = models.IntegerField(blank=True)
    positive = models.IntegerField(blank=True)
    positive_cases_viral = models.IntegerField(blank=True)
    positive_increase = models.IntegerField(blank=True)
    positive_score = models.IntegerField(blank=True)
    positive_tests_antibody = models.IntegerField(blank=True)
    positive_tests_antigen = models.IntegerField(blank=True)
    positive_tests_people_antibody = models.IntegerField(blank=True)
    positive_tests_people_antigen = models.IntegerField(blank=True)
    positive_tests_viral = models.IntegerField(blank=True)
    recovered = models.IntegerField(blank=True)
    total_test_encounters_viral = models.IntegerField(blank=True)
    total_test_encounters_viral_increase = models.IntegerField(blank=True)
    total_test_results = models.IntegerField(blank=True)
    total_test_results_increase = models.IntegerField(blank=True)
    total_tests_antibody = models.IntegerField(blank=True)
    total_tests_antigen = models.IntegerField(blank=True)
    total_tests_people_antibody = models.IntegerField(blank=True)
    total_tests_people_antigen = models.IntegerField(blank=True)
    total_tests_people_viral = models.IntegerField(blank=True)
    total_tests_people_viral_increase = models.IntegerField(blank=True)
    total_tests_viral = models.IntegerField(blank=True)
    total_tests_viral_increase = models.IntegerField(blank=True)
