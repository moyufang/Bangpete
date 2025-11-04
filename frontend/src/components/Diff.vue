<script setup>
const props = defineProps({
  diff: {
    type: Array,
    required: true,
    validator: (value) => value.length === 5
  }
})
const diff = props.diff;
</script>

<template>
<div class="diff">
  <span class="diff-item easy">{{ diff[0] }}</span>
  <span class="diff-item normal">{{ diff[1] }}</span>
  <span class="diff-item hard">{{ diff[2] }}</span>
  <span class="diff-item expert">{{ diff[3] }}</span>
  <span v-if="diff[4]>-1"
        class="diff-item special">{{ diff[4] }}</span>
</div>
</template>

<style scoped lang='scss'>


.diff{
  background: none;
  width: fit-content;
  height: fit-content;

  @include flex('row', 'center', 'center');
  gap: $spacing-md;

  & .diff-item{
    width: $diff-size;
    height: $diff-size;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: black;
    font-size: $diff-font-size;

    &.easy { background-color: $diff-color-easy; }
    &.normal { background-color: $diff-color-normal; }
    &.hard { background-color: $diff-color-hard; }
    &.expert { background-color: $diff-color-expert; }
    &.special { background-color: $diff-color-special; }
  }
}


</style>