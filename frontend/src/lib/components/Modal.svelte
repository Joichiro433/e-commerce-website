<script lang="ts">
  export let closeModal: () => void;
</script>

<div class="modal-overlay">
  <div class="modal">
    <div class="modal-content">
      <slot />
    </div>
    <div class="button-container">
      <button on:click={closeModal}>Close</button>
    </div>
  </div>
</div>

<style>
  /* Modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background: white;
    border-radius: 8px;
    width: 80%;
    max-width: 400px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
  }

  .modal-content {
    padding: 2rem;
    flex-grow: 1;
  }

  .button-container {
    display: flex;
    justify-content: flex-end; /* Aligns the button to the right */
    padding: 1rem; /* Adjusts the padding as needed */
  }
</style>
