import Cookies from 'js-cookie';
import * as ApiX from "@snowind/api";

export default class Api extends ApiX.default {

  setCsrfStatus(verbose = false): boolean {
    if (verbose) {
      console.log("Checking login status from cookie")
    }
    if (this.hasCsrfCookie) {
      if (verbose) {
        console.log("User logged in with csrf cookie, setting api token");
      }
      this.setCsrfToken(verbose);
      return true
    }
    if (verbose) {
      console.log("User does not have csrf cookie")
    }
    return false;
  }

  async login(username: string, password: string, autoLogOut = false): Promise<Record<string, any>> {
    let url = this.serverUrl + "/auth/login/";
    const payload = {
      username: username,
      password: password,
    }
    const opts = this.postHeader(payload);
    const response = await fetch(url, opts);
    if (!response.ok) {
      if (autoLogOut) {
        //console.log("Autologout", response.status)
        if (response.status === 403) {
          throw new Error(`${response}`);
        }
      }
      //console.log("Django login RESP NOT OK", response);
      throw new Error(response.toString());
    }
    const data = await response.json() as Record<string, any>;
    return data;
  }

  async logout() {
    const uri = this.serverUrl + "/auth/logout/";
    //console.log("Logout", uri)
    const response = await fetch(uri, this.header("get"));
    if (!response.ok) {
      throw new Error(`Server logout failed ${response}`);
    }
    Cookies.remove(this.csrfCookieName);
  }
}

