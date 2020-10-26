
def format_datetime(value,fmt='%Y년 %m월 %d일'):
    return value.strftime(fmt)
# %H:%M

def exchange_rate(value):
    result =''
    try :
        value = int(value)

        if value>=10000:

            if value >= 100000000:
                auk = value // 100000000
                value = value % 100000000
                result +=str(auk)+'억'

            man = value //10000
            result +=str(man)+'만'

            won = value % 10000
            if won != 0:
                result +=str(won)+'원'
            else :
                result +='원'
        else:
            value = '{}원'.format(value)
            return value
    except:
       result = value

    return result