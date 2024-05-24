/**
 * @param {string}
 * @returns {string}
 */
const hello = (name) => `hello ${name}`;

hello("dcai");

/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @typedef {Object} ListNode
 * @property {ListNode} val
 * @property {ListNode} next
 * @param {ListNode} l1
 * @param {ListNode} l2
 * @return {ListNode}
 */
function toArray(input) {
  let l = input;
  const arr = [l.val];
  while (l.next !== null) {
    l = l.next;
    arr.push(l.val);
  }
  return arr;
}
const toLinkList = (arr) =>
  arr.reverse().reduce((next, val) => {
    return { val, next };
  }, null);

const toNum = (v) => {
  if (v === undefined || v === null) return 0;
  return v;
};

const addTwoNumbers = function (li1, li2) {
  const target = [];
  l1 = toArray(li1);
  l2 = toArray(li2);
  const size = l1.length > l2.length ? l1.length : l2.length;
  let addOne = 0;
  for (let i = 0; i < size; i++) {
    const sum = toNum(l1[i]) + toNum(l2[i]) + addOne;
    target.push(sum < 10 ? sum : sum - 10);
    addOne = sum - 10 >= 0 ? 1 : 0;
  }
  if (addOne !== 0) {
    target.push(1);
  }
  return toLinkList(target);
};

const result = addTwoNumbers(
  toLinkList([9, 9, 9, 9, 9, 9, 9]),
  toLinkList([9, 9, 9, 9]),
);
console.log(`result: ${result}`);
