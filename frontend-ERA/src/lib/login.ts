var login: string = ""

export async function change_user(new_user: string): Promise<void>{
    const response = await fetch(`http://localhost:8000/user/${new_user}`);
    const data = await response.json();

    const obj = JSON.parse(data)

    if(obj.username != "null"){
        login = obj.username
    }
}

export function get_user(): string {
    return login
}