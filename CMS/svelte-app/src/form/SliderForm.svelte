<script>
    import {writable} from "svelte/store";
    import "tw-elements";
    import {Net} from "../net";

    export let sliderData;
    export let formNet;

    let slides = sliderData.slides;

    formNet.slider = slides

    function swapUp(i) {
        if (i !== 0) {
            const tmp = slides[i - 1];
            slides[i - 1] = slides[i];
            slides[i] = tmp;
        }
    }

    function swapDown(i) {
        if (i !== slides.length - 1) {
            const tmp = slides[i + 1];
            slides[i + 1] = slides[i];
            slides[i] = tmp;
        }
    }

    const newsFormValues = writable({
        title: "",
        description: "",
        src: "",
        position: slides.length + 1,
    });

    function newsFormSubmit() {
        const obj = {
            title: $newsFormValues.title,
            description: $newsFormValues.description,
            src: $newsFormValues.src.replace("C:\\fakepath\\",''),
        };
        let position = $newsFormValues.position;

        if (formStatus !== -1) del(formStatus);

        console.log(file)

        if(file != null) Net.sendPhoto(obj.src, file)


        file = null

        slides.splice(position - 1, 0, obj);
        slides = slides;

        console.log(slides, slides.length + 1);
        $newsFormValues.title = "";
        $newsFormValues.description = "";
        $newsFormValues.src = "";
        $newsFormValues.position = slides.length + 1;
    }

    let formStatus = -1; //-1: adding new news; <=0 : editing selected index

    function edit(i) {
        const obj = slides[i];
        formStatus = i;
        $newsFormValues.title = obj.title;
        $newsFormValues.description = obj.description;
        $newsFormValues.src = obj.src;
        $newsFormValues.position = i + 1;
    }

    function del() {
        slides.splice(formStatus, 1);
        slides = slides;
        cancel();
    }

    function cancel() {
        $newsFormValues.title = "";
        $newsFormValues.description = "";
        $newsFormValues.src = "";
        $newsFormValues.position = slides.length + 1;
        formStatus = -1;
    }

    let file;

    function onFileSelected(e) {
        file = e.target.files[0];
    }
</script>

<div class="border border-gray-300 m-10 px-10 pb-10">
    <h1 class="p-5">Slider Form</h1>
    <div class="flex flex-row">
        <form
                on:submit|preventDefault={() => newsFormSubmit()}
                class="w-1/3  border border-gray-300"
        >
            <h3 class="m-4">
                {#if formStatus === -1}
                    Adding new element:
                {:else}
                    Editing element: (title:{slides[formStatus].title}
                {/if}
            </h3>
            <div class="m-4">
                <label>title<input
                        type="text"
                        bind:value={$newsFormValues.title}
                        class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                /></label>
            </div>
            <div class="m-4">
                <label>description<textarea
                        type="text"
                        bind:value={$newsFormValues.description}
                        class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"></textarea></label>
            </div>
            <div class="m-4">
                <label>src
                    <input type="file" accept=".jpg, .jpeg, .png"
                           on:change={(e)=>onFileSelected(e)}
                           bind:value={$newsFormValues.src}
                           class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                           id="formFile"></label>
            </div>
            <div class="m-4">
                <label>position<input
                        type="number"
                        min="1"
                        max={formStatus === -1 ? slides.length + 1 : slides.length}
                        bind:value={$newsFormValues.position}
                        class=" form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                /></label>
            </div>
            <div class="flex flex-row">
                <button
                        type="submit"
                        class="m-4 px-6 py-2.5 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
                >
                    Submit
                </button>

                {#if formStatus !== -1}
                    <button
                            on:click={del}
                            type="button"
                            class="inline-block px-6 py-2 border-2 border-red-600 text-red-600 font-medium text-xs leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out"
                    >
                        Delete
                    </button>
                    <button
                            on:click={cancel}
                            type="button"
                            class="inline-block px-6 py-2 border-2 border-yellow-500 text-yellow-500 font-medium text-xs leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out"
                    >
                        Cancel
                    </button>
                {/if}
            </div>
        </form>

        <table class="ml-4 content-list w-2/3">
            <tr>
                <th class="border border-slate-300">title</th>
                <th class="border border-slate-300">description</th>
                <th class="border border-slate-300">file</th>
                <th class="border border-slate-300">edit</th>
            </tr>
            {#each slides as oneSlide, i}
                <tr>
                    <td
                            class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap"
                    >{oneSlide.title}</td
                    >
                    <td
                            class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4"
                    >{oneSlide.description}</td
                    >
                    <td
                            class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap"
                    >{oneSlide.src}</td
                    >
                    <td
                            class="border border-slate-300 text-sm text-gray-900 font-light px-3 py-1 whitespace-nowrap"
                    >
                        <div class="flex flex-row justify-around">
                            <button
                                    on:click={() => edit(i)}
                                    class="edit px-4 uppercase">edit
                            </button
                            >
                            <div class="flex flex-col">
                            </div>
                        </div>
                    </td>
                </tr>
            {/each}
        </table>
    </div>
</div>

<style>
    .edit:hover,
    .arrow:hover svg {
        color: #00e9ff;
    }

    .content-list tr:nth-child(2) .arrow:first-child svg {
        opacity: 0.3;
    }

    .content-list tr:last-child .arrow:last-child svg {
        opacity: 0.3;
    }

    .content-list tr:nth-child(2) .arrow:first-child:hover svg {
        opacity: 0.3;
        color: black;
    }

    .content-list tr:last-child .arrow:last-child:hover svg {
        opacity: 0.3;
        color: black;
    }
</style>
