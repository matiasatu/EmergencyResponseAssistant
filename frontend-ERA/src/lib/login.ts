var login: string = ""

export async function change_user(new_user: string): Promise<boolean>{
    const response = await fetch(`/api/user/${new_user}`);
    const data = await response.json();

    const obj = JSON.parse(data)

    if(obj.username != "null"){
        login = obj.username
        return true
    }

    return false
}

export function get_user(): string {
    return login
}

export function logout(): void {
    login = ""
}