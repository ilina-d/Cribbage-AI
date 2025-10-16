import os
from sty import fg as Text, bg as Back, rs as Rest


os.system('')

input()

print(f'{Back.white}{Text.red} ♥     {Rest.all} ' * 6)
print(f'{Back.white}{Text.red}       {Rest.all} ' * 6)
print(f'{Back.white}{Text.red}   5   {Rest.all} ' * 6)
print(f'{Back.white}{Text.red}       {Rest.all} ' * 6)
print(f'{Back.white}{Text.red}     ♥ {Rest.all} ' * 6)
print('\n\n')

print(f'{Back.white}     {Rest.all}')
print(f'{Back.white}{Text.red}  ♥  {Rest.all}')
print(f'{Back.white}{Text.red}  5  {Rest.all}')
print(f'{Back.white}     {Rest.all}\n\n')


print(f'{Back.white}     {Rest.all}')
print(f'{Back.white}{Text.black}  ♠  {Rest.all}')
print(f'{Back.white}{Text.black}  K  {Rest.all}')
print(f'{Back.white}     {Rest.all}\n\n')

print('♣ ♦ ♠ ♥')
input()
