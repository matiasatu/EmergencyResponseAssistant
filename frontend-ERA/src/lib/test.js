import * as login from './login.ts'


await login.change_user('matias')
console.log(login.get_user());
