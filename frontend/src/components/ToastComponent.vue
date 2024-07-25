<template>
  <div></div>
</template>

<script>
import { useToast } from "vue-toastification";
import "vue-toastification/dist/index.css";

export default {
  setup() {
    const toast = useToast();

    const showMessage = ({ messages, type }) => {
      if (type === "error") {
        // Show error message
        toast.error(getErrorMessages(messages));
      } else if (type === "warn") {
        // Show warning message
        toast.warning(getWarningMessage(messages));
      } else {
        // Show success message
        toast.success(getSuccessMessage(messages));
      }
    };

    const getErrorMessages = (messages) => {
      if (Array.isArray(messages)) {
        if (messages.length > 0) {
          return messages.join("\n");
        }
      } else if (typeof messages === "string") {
        return messages;
      }
      return ""; // Return an empty string if there are no messages
    };

    const getSuccessMessage = (messages) => {
      return messages;
    };

    const getWarningMessage = (messages) => {
      return messages;
    };

    return {
      showMessage,
    };
  },
};
</script>
