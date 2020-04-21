from rest_framework import serializers

from .models import Question, Questionnaire, Questionnaire_content

class QuestionSerializer(serializers.ModelSerializer):  
    
    class Meta:  
        model = Question  
        fields = '__all__'



class Questionnaire_contentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questionnaire_content
        fields = ('question', 'time_to_answer', 'answer_weight')



class QuestionnaireSerializer(serializers.ModelSerializer):
    
    questions = Questionnaire_contentSerializer(source='questionnaire_content_set', many=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'name', 'time_to_live', 'questions', 'target_users')
    
    def create(self, validated_data):
        questionnaire_content_set = validated_data.pop('questionnaire_content_set')
        questionnaire = Questionnaire.objects.create(
            name=validated_data['name'],
            time_to_live=validated_data['time_to_live'],
        )
        questionnaire.target_users.set(validated_data['target_users '])
        for questionnaire_content_od in questionnaire_content_set:
            questionnaire_content = dict(questionnaire_content_od)
            Questionnaire_content.objects.create(
                questionnaire=questionnaire,
                question=questionnaire_content['question'], 
                time_to_answer=questionnaire_content['time_to_answer'], 
                answer_weight=questionnaire_content['answer_weight']
            )
        return questionnaire

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.time_to_live = validated_data.get('time_to_live', instance.time_to_live)
        instance.target_users.set(validated_data.get('target_users', instance.target_users))
        instance.save()

        Questionnaire_content.objects.filter(questionnaire=instance).delete()
        for questionnaire_content_od in validated_data['questionnaire_content_set']:
            questionnaire_content = dict(questionnaire_content_od)
            Questionnaire_content.objects.create(
                questionnaire=instance, 
                question=questionnaire_content['question'], 
                time_to_answer=questionnaire_content['time_to_answer'], 
                answer_weight=questionnaire_content['answer_weight']
                )
        return instance
