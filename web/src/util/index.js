import router from "@/router"
import useMenuStore from "@/store/menus"


export const getJWT=()=>{
    if(localStorage.getItem('JWT')){
        return `Bearer ${localStorage.getItem('JWT')}` 
    }else{
        return null
    }
}

export const setJWT=(jwt)=>{
    localStorage.setItem('JWT',jwt)
    const menuStore = useMenuStore()
    menuStore.setMenuList([])
}

export const rmJWT = () => {
  localStorage.removeItem("JWT")
  router.replace({name:'login'})
}

export const getCookie = function (name) {
    var value = '; ' + document.cookie
    var parts = value.split('; ' + name + '=')
    if (parts.length === 2) return parts.pop().split(';').shift()
}


