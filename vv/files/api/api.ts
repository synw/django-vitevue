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

  async login(username: string, password: string, url = "/vv/auth/login/"): Promise<boolean> {
    let _url = this.serverUrl + url;
    const payload = {
      username: username,
      password: password,
    }
    const opts = this.postHeader(payload);
    const response = await fetch(_url, opts);
    if (!response.ok) {
      return false
    }
    return true
  }

  async logout(url = "/vv/auth/logout/") {
    const _url = this.serverUrl + url;
    //console.log("Logout", uri)
    const response = await fetch(_url, this.header("get"));
    if (!response.ok) {
      throw new Error(`Server logout failed ${response}`);
    }
    Cookies.remove(this.csrfCookieName);
  }
}

