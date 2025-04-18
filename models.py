from django.db import models
#from simplecep.fields import CEPField

class Cliente(models.Model):
    nome = models.CharField(max_length=72)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=14)
    cpf = models.CharField(max_length=14)  # Tamanho com pontuação
    rg = models.CharField(max_length=14, blank=True, null=True)
    instagram = models.CharField(max_length=32, blank=True, null=True)
    telegram = models.CharField(max_length=32, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    dta_cadastro = models.DateTimeField(auto_now_add=True)
    dta_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')  # Muitos para um
    rua = models.CharField(max_length=96)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=96)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9) # models.CharField(max_length=9) #cep = CEPField()  # Campo de CEP da biblioteca
    ativo = models.BooleanField(default=True)
    dta_cadastro = models.DateTimeField(auto_now_add=True)
    dta_atualizacao = models.DateTimeField(auto_now=True)
    tipo = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.tipo} - {self.rua}, {self.numero}, {self.complemento}, {self.bairro}, {self.cidade}, {self.estado} - {self.cep}"


class Item(models.Model):
    descricao = models.CharField(max_length=96)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    peso = models.DecimalField(max_digits=5, decimal_places=3)
    altura = models.PositiveIntegerField(default=0)
    largura = models.PositiveIntegerField(default=0)
    comprimento = models.PositiveIntegerField(default=0)
    estoque = models.IntegerField()
    status = models.BooleanField(default=True)  # Adicionei o campo status
    dta_cadastro = models.DateTimeField(auto_now_add=True)
    dta_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.descricao

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    itens = models.ManyToManyField(Item, related_name='pedidos')   #item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    valor_frete = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    canal_venda = models.CharField(max_length=28)
    tipo_frete = models.CharField(max_length=32)
    rastreio_frete = models.CharField(max_length=254, blank=True, null=True)
    status_frete = models.CharField(max_length=32)
    ativo = models.BooleanField(default=True)
    dta_cadastro = models.DateTimeField(auto_now_add=True)
    dta_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"

class Pagamento(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=18)
    sinal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=18)
    dta_cadastro = models.DateTimeField(auto_now_add=True)
    dta_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pagamento {self.pedido.id} - {self.tipo} - {'Pago' if self.status else 'Pendente'}"
