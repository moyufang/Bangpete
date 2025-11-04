<script setup lang="ts">
interface Props {
  diff: number[]
}

const props = defineProps<Props>()

// 验证 diff 数组长度
if (props.diff.length !== 5) {
  console.warn('Diff component expects an array of 5 numbers')
}
</script>

<template>
  <div class="diff">
    <span class="diff-item easy">{{ props.diff[0] }}</span>
    <span class="diff-item normal">{{ props.diff[1] }}</span>
    <span class="diff-item hard">{{ props.diff[2] }}</span>
    <span class="diff-item expert">{{ props.diff[3] }}</span>
    <span 
      v-if="props.diff[4] > -1"
      class="diff-item special"
    >
      {{ props.diff[4] }}
    </span>
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