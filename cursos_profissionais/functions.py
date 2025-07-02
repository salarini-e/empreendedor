import asyncio
import aiohttp

def validar_nome(self):
    if len(self.nome.split()) < 2:
        return False
    return True
    
async def fazer_requisicao_post(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()