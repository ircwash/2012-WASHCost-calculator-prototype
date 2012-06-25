from django import template

register = template.Library()

def yearly_growth(value, exponent):
    value = int(value)
    exponent = float(exponent)
    
    years = [value]
    for _ in xrange(1, 20):
        value = value * ( 1 + exponent/100 )
        years.append(value)
    
    return years

register.filter('yearly_growth', yearly_growth)