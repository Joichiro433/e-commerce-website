import { writable } from 'svelte/store';

// ブラウザ環境かどうかを判定する関数
function isBrowser() {
  return typeof window !== 'undefined';
}

let initialLoginState = false;

// ブラウザ環境の場合のみlocalStorageからの読み取りを行う
if (isBrowser()) {
  initialLoginState = localStorage.getItem('isLogin') === 'true';
}

export const isLogin = writable(initialLoginState);

// isLoginの値が変わるたびにlocalStorageを更新する
isLogin.subscribe((value) => {
  if (isBrowser()) {
    localStorage.setItem('isLogin', value.toString());
  }
});
