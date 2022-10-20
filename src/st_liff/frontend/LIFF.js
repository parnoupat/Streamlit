function logOut() {
    liff.logout()
    window.location.reload()
  }
  function logIn() {
    liff.login({ redirectUri: window.location.href })
  }
  async function getUserProfile() {
    const profile = await liff.getProfile()
    document.getElementById("pictureUrl").style.display = "block"
    document.getElementById("pictureUrl").src = profile.pictureUrl
  }
  async function main() {
    await liff.init({ liffId: "YOUR-LIFF-ID" })
    if (liff.isInClient()) {
      getUserProfile()
    } else {
      if (liff.isLoggedIn()) {
        getUserProfile()
        document.getElementById("btnLogIn").style.display = "none"
        document.getElementById("btnLogOut").style.display = "block"
      } else {
        document.getElementById("btnLogIn").style.display = "block"
        document.getElementById("btnLogOut").style.display = "none"
      }
    }
  }
  main()