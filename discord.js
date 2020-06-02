// Copy and paste snippets from here on the developer console
// which resides on the discord app (Ctrl+Shift+I).	


let leaveAllGroups = function() {
    document
        // Matches each "exit" button from each channel entry.
        .querySelectorAll("header ~ div[class*='channel-'] button")
        .forEach((button) => {
            button.click();
            confirmation = document.querySelector("button[type='submit']");
            if (confirmation !== null)
                confirmation.click();
        });
};
