import endpoint from "./constants";

async function conection(url){
    let data = {};
    let text = [];

    try{
        data = await fetch(url);
    } catch(error){
        console.log(error);
    }

    if(!data.ok){
        text = "Fallo al conectar con el servidor";
    } else {
        text = await data.json();
    }

    return text;
}

export async function login(){
    data = await conection(endpoint.login);
}