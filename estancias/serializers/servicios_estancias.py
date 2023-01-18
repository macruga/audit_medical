from rest_framework import serializers


from estancias.models.servicios_estancias import ServiciosEstanciaModel



class ServiciosEstanciaSerializer(serializers.ModelSerializer):
     # Save owner

    active = serializers.HiddenField(
        default=True
        )
   


    class Meta:
        model= ServiciosEstanciaModel
        fields = '__all__'