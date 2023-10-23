<script lang="ts">
  import { goto } from '$app/navigation';
  import { isLogin } from '$lib/stores/loginStatus';
  import Api from '$lib/api';
  import logger from '$lib/logger';

  $: email = '';
  $: password = '';
  let loginError = false;

  const handleLogin = async (): Promise<void> => {
    const data = new URLSearchParams();
    data.append('username', email);
    data.append('password', password);
    try {
      const resp = await Api.post('/login', data, { contentType: 'application/x-www-form-urlencoded' });
      if (resp.status == 200) {
        $isLogin = true;
        goto('/');
      }
    } catch (e) {
      if (Api.verifyAxiosError(e) && e.response?.status === 401) {
        loginError = true;
      } else {
        logger.error('Failed to handleLogin:', e);
        alert('エラーが発生しました。ページをリロードしてもう一度お試しください。');
      }
    }
  };
</script>

<form>
  <h2>Log In</h2>
  <div>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required bind:value={email} />
  </div>

  <div>
    <label for="password">Password:</label>
    <input type="password" id="password" name="password" required bind:value={password} />
  </div>

  {#if loginError}
    <p class="error-message">メールアドレスまたはパスワードが一致しません。</p>
  {/if}

  <div>
    <button type="submit" on:click|preventDefault={handleLogin}>Login</button>
  </div>

  <div>
    <p style="text-align: center;">
      <a href="/signup" on:click|preventDefault={() => goto('/signup')}>Create an account</a>
    </p>
  </div>
</form>

<style>
  form {
    max-width: 400px;
    margin: 4rem auto;
    padding: 2rem;
    border: 1px solid #f1f1f1;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  h2 {
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: #9b4dca;
  }

  div {
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }

  input {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  a {
    color: #9b4dca;
    text-decoration: underline;
    cursor: pointer;
  }

  .error-message {
    color: red;
    font-size: 15px;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
  }
</style>
