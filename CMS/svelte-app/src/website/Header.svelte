<script>
    export let headerData;
    import {Net} from "../net";

</script>

<header class="text-gray-600 body-font" style="    width: 100%;
    display: flex;
    justify-content: space-around;">
    <div class="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
        <div class="flex title-font font-medium items-center text-gray-900 mb-4 md:mb-0">
            {#if headerData["logo"] !== undefined}
                {#await Net.fetchPhoto(headerData.logo.src)}
                    Loading photo...
                {:then photo}
                    <img style="width:{headerData.logo.width}; height:{headerData.logo.height}" fill="none"
                         stroke="currentColor"
                         stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                         class="w-10 h-10 text-white p-2 bg-indigo-500 rounded-full" viewBox="0 0 24 24"
                         src={photo} alt={headerData.logo.src}>
                {/await}
            {/if}
        </div>
        <nav class="md:mr-auto md:ml-4 md:py-1 md:pl-4 md:border-l md:border-gray-400	flex flex-wrap items-center text-base justify-center">
            {#each headerData.menu.links as link}
                {#if link.dropDown}
                    <div class="drop-down">
                        <a href={link.href}>{link.text}</a>
                        <ul>
                            {#each link.content as subLink}
                                <li><a href={subLink.href}>{subLink.text}</a></li>
                            {/each}
                        </ul>
                    </div>
                {:else}
                    <a href={link.href}>{link.text}</a>
                {/if}
            {/each}
        </nav>
    </div>
</header>
<style>
    a {
        margin: 10px;
    }

    a:visited{
    text-decoration: none;
    color:black;
}

    .drop-down ul {
        display: none;
        /*background-color: #9ca3af;*/
        position: absolute;
    }

    .drop-down:hover ul {
        display: block;
    }

    .drop-down ul:hover {
        display: block;
    }

</style>