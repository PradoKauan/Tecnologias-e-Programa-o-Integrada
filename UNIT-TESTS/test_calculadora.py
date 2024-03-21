import calculadora 
import pytest

def teste_soma():
    resultado = calculadora.soma(-1,2)
    assert resultado == 1
    

def teste_soma_invalido():
    with pytest.raises(ValueError) as excinfo:  
        calculadora.soma(-1,'a') 
    assert str(excinfo.value) == "Valor digitado esta incorreto"

def teste_sub():
    resultado = calculadora.sub(2,1)
    assert resultado == 1

def teste_sub_invalido():
    with pytest.raises(ValueError) as excinfo:  
        calculadora.sub(-1,'a') 
    assert str(excinfo.value) == "Valor digitado esta incorreto"

def teste_div():
    resultado = calculadora.div(10,2)
    assert resultado == 5

def teste_div_invalido():
    with pytest.raises(ValueError) as excinfo:  
        calculadora.div(-1,'a') 
    assert str(excinfo.value) == "Valor digitado esta incorreto"

def teste_mult():
    resultado = calculadora.mult(1,2)
    assert resultado == 2

def teste_mult_invalido():
    with pytest.raises(ValueError) as excinfo:  
        calculadora.mult(-1,'a') 
    assert str(excinfo.value) == "Valor digitado esta incorreto"
